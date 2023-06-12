from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, ForgotPasswordSerializer, VerifyTokenSerializer
from .models import User
from .utils import authenticate_token
from watchpartyapp.models import PartyGroup


class Register(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(user.get_tokens(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    # permission_classes = [permissions.]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            return Response({'code': user.forgot_password_code()}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyToken(generics.GenericAPIView):
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            authenticated, user = authenticate_token(request.data['access'])
            if authenticated:
                return Response({'message': 'valid', 'email': user.email}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Change(generics.GenericAPIView):
    def get(self, request):
        group = PartyGroup.objects.get(id='d036cb034a781b44a54832f0')
        group.url = 'https://www.fb.com/'
        group.save()
        return Response({'message': 'done'}, status=status.HTTP_200_OK)