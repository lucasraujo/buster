from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from .serializer import MoviesSerializer, MovieOrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from .models import Movie
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class customPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_employee


class MoviesView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [customPermission]

    def post(self, request):
        serializer = MoviesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        allMovies = Movie.objects.all()
        result_page = self.paginate_queryset(allMovies, request, view=self)
        serializer = MoviesSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MoviesDatailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [customPermission]
    
    def get(self, request, movie_id):
        movie_find = get_object_or_404(Movie, id=movie_id)
        serializer = MoviesSerializer(movie_find)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, movie_id):
        movie_find = get_object_or_404(Movie, id=movie_id)
        movie_find.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MovieOrderDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, movie_id):
        movie_find = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(users_ordes=request.user, movies_orders=movie_find)
        return Response(serializer.data, status=status.HTTP_201_CREATED)