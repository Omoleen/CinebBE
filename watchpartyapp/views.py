from rest_framework import generics, status, permissions
from rest_framework.response import Response
from userapp.models import User
from .models import PartyGroup
from .serializers import PartyGroupSerializer


class WatchParty(generics.GenericAPIView):

    # create watch party
    def post(self, request):
        return Response()

    # exit watch party
    def delete(self, request):
        return Response()

    # def patch(self, request):
    #     return self.


class GroupParty(generics.RetrieveUpdateDestroyAPIView):
    queryset = PartyGroup.objects.all()
    serializer_class = PartyGroupSerializer
    lookup_field = 'pk'
