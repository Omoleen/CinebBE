import asyncio

from .models import PartyGroupMessage, PartyGroup
from userapp.models import User
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from .serializers import PartyGroupMessagesSerializer, PartyGroupSerializer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.consumers import AsyncAPIConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication


def authenticate_token(token) -> User or None:
    try:
        decoded_token = AccessToken(token)
        decoded_token.verify()
    # except TokenExpired:
    #     raise InvalidToken('Token has expired')
    except:
        # raise InvalidToken('Token is invalid')
        return None
    else:
        user = JWTAuthentication().get_user(decoded_token)
        if user is not None:
            return user
        else:
            # raise InvalidToken('User not found')
            return None


async_authenticate_token = sync_to_async(authenticate_token)


class ChatConsumer(GenericAsyncAPIConsumer):

    @model_observer(PartyGroupMessage)
    async def chat_activity(
        self,
        message,
        observer=None,
        subscribing_request_ids=[],
        **kwargs
    ):
        await self.send_json(message)

    @chat_activity.serializer
    def chat_activity(self, instance: PartyGroupMessage, action, **kwargs):
        '''This will return the comment serializer'''
        return PartyGroupMessagesSerializer(instance).data

    @chat_activity.groups_for_signal
    def chat_activity(self, instance: PartyGroupMessage, **kwargs):
        # this block of code is called very often *DO NOT make DB QUERIES HERE*
        yield f'-group__{instance.partyGroup.id}_chat'

    @chat_activity.groups_for_consumer
    def chat_activity(self, partyGroup, **kwargs):
        # This is called when you subscribe/unsubscribe
        yield f'-group__{partyGroup.id}_chat'

    def get_user_name_and_admin(self, user, partygroup):
        return user.name, partygroup.adminUser

    def get_past_messages(self, partygroup):
        return PartyGroupMessagesSerializer(partygroup.messages.all(), many=True).data

    def update_party_users(self, partygroup, add=True):
        if add:
            partygroup.num_of_users += 1
        else:
            partygroup.num_of_users -= 1
        partygroup.save()
    @action()
    async def subscribe_to_chat_activity(self, request_id, partyId, **kwargs):
        try:
            print(id)
            partygroup = await PartyGroup.objects.aget(id=partyId)
            if kwargs.get('accessToken') is not None:
                user = await async_authenticate_token(kwargs.get('accessToken'))
            else:
                user = None
            past_messages = await sync_to_async(self.get_past_messages)(partygroup)
            await self.send_json(past_messages)
            await self.send_json({
                'partyUrl': partygroup.url,
                'partyId': partygroup.id,
                'num_of_users': partygroup.num_of_users
            })
            await self.chat_activity.subscribe(partyGroup=partygroup, request_id=request_id)
            if user is not None:
                name, admin = await sync_to_async(self.get_user_name_and_admin)(user, partygroup)
                if admin != user:
                    await database_sync_to_async(PartyGroupMessage.objects.create)(partyGroup=partygroup, message=f'{name} joined the watch party!', message_from_machine=True)
                    await database_sync_to_async(self.update_party_users)(partygroup)

        except PartyGroup.DoesNotExist:
            await self.send_json({
                'error': 'invalid group'
            }, 1000)

    @action()
    async def send_message(self, request_id, partyId, message, **kwargs):
        try:
            partygroup = await PartyGroup.objects.aget(id=partyId)
            if kwargs.get('accessToken') is not None:
                user = await async_authenticate_token(kwargs.get('accessToken'))
            else:
                user = None
            mess = await PartyGroupMessage.objects.acreate(partyGroup=partygroup, message=message, message_from_user=user)
        except PartyGroup.DoesNotExist:
            await self.send_json({
                'error': 'invalid group'
            }, 1000)

    @action()
    async def admin_close_group(self, request_id, **kwargs):
        if kwargs.get('partyId') is None:
            await self.send_json({
                'error': 'input partyID'
            }, 1000)
        if kwargs.get('accessToken') is not None:
            user = await async_authenticate_token(kwargs.get('accessToken'))
            if user is not None:
                group = await user.party_group.aget(id=kwargs.get('partyId'))
                if group:
                    await self.send_json({
                        'alert': 'group closed'
                    }, 1000)
                    await database_sync_to_async(group.delete)()
                else:
                    await self.send_json({
                        'error': "you don't have admin access to this group"
                    }, 1000)
            else:
                await self.send_json({
                    'error': "user does not exist"
                }, 1000)

        else:
            await self.send_json({
                'error': 'you cannot close this group because you are not an admin'
            }, 1000)

    @action()
    async def unsubscribe_from_chat_activity(self, request_id, partyId, **kwargs):
        try:
            partygroup = await PartyGroup.objects.aget(id=partyId)
            await self.chat_activity.unsubscribe(partyGroup=partygroup, request_id=request_id)
            await self.send_json({
                'message': 'group exited'
            }, 1000)
            await database_sync_to_async(self.update_party_users)(partygroup, False)

        except PartyGroup.DoesNotExist:
            await self.send_json({
                'error': 'invalid group'
            }, 1000)

    @action()
    async def create_group(self, request_id, **kwargs):
        if kwargs.get('accessToken') is not None:
            user = await async_authenticate_token(kwargs.get('accessToken'))
            if user is not None:
                if await database_sync_to_async(user.party_group.exists)():
                    group = await database_sync_to_async(user.party_group.first)()
                else:
                    group = await database_sync_to_async(user.party_group.create)(url=kwargs.get('partyUrl'))
                await self.send_json({
                    'partyId': group.id,
                    'alert': 'group created',
                    'partyUrl': group.url
                })
            else:
                await self.send_json({
                    'error': "user does not exist"
                }, 1000)

        else:
            await self.send_json({
                'error': "you cannot create a group because you don't have an account"
            }, 1000)


class GroupConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = PartyGroup.objects.all()
    serializer_class = PartyGroupSerializer

    @action()
    async def subscribe_instance(self, request_id, **kwargs):
        partygroup = await PartyGroup.objects.aget(pk=kwargs.get('pk'))
        await self.send_json({'data': PartyGroupSerializer(partygroup).data})

        await super().subscribe_instance(request_id, **kwargs)

    # def update_time(self, partygroup, time):


    # @action()
    # async def set_time(self, request_id, current_time, **kwargs):
    #     partygroup = await PartyGroup.objects.aget(pk=kwargs.get('pk'))
    #     partygroup.current_time = current_time
    #     await partygroup.asave()
    #     await self.send_json({
    #         'message': 'time updated'
    #     })
    #
    # @action()
    # async def set_is_playing(self, request_id, is_playing, **kwargs):
    #     partygroup = await PartyGroup.objects.aget(pk=kwargs.get('pk'))
    #     partygroup.is_playing = is_playing
    #     await partygroup.asave()
    #     await self.send_json({
    #         'message': 'is_playing updated'
    #     })