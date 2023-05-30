from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .serializer import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsOwnerOfAcount(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return request.user == obj or request.user.is_employee


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOfAcount]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(
            instance=user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
