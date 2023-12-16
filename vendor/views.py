from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, generics, status

from django.contrib.auth import login, logout

from utils.permissions import IsAPIKEYAuthenticated


from .models import Vendor
from .serializers import (CreateVendorSerialzier,
                          ChangePasswordSerializer,
                          LoginUserSerializer,
                          VendorSerializer,
                          VendorLoginSerializer)


class LoginAPI(generics.CreateAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny, IsAPIKEYAuthenticated)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            serializer = VendorLoginSerializer(user)

            serialized_data = serializer.data
            serialized_data['token'] = token.key

            return Response(serialized_data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAPIKEYAuthenticated)
    serializer_class = VendorSerializer

    def update(self, request, *args, **kwargs):
        if int(kwargs['pk']) != self.request.user.id:
            return Response({"error": "Invalid vendor id"}, status=status.HTTP_400_BAD_REQUEST)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAPIKEYAuthenticated]
    serializer_class = VendorSerializer

    def get_object(self):
        return self.request.user


class VendorListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, IsAPIKEYAuthenticated)
    serializer_class = VendorSerializer

    def get_queryset(self):
        return Vendor.objects.all()


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAPIKEYAuthenticated, )

    def delete(self, request):
        request.auth.delete()
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class VendorDeleteAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class Register(APIView):
    permission_classes = (permissions.AllowAny, IsAPIKEYAuthenticated, )

    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        password = self.request.data.get('password', False)

        if phone and password:
            phone = str(phone)
            user = Vendor.objects.filter(phone__iexact = phone)

            if user.exists():
                return Response({
                    'error': 'Phone Number already have account associated.'
                    })

            else:
                serializer = CreateVendorSerialzier(data=self.request.data)
                serializer.is_valid(raise_exception = True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({
                'error' : 'Either phone or password was not recieved in Post request'
            })
