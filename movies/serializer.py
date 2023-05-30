from rest_framework import serializers
from .models import RatingChoices
from users.serializer import UserSerializer
from .models import Movie, MovieOrder


class MoviesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10, default=None)
    rating = serializers.ChoiceField(choices=RatingChoices.choices, default=RatingChoices.G)
    synopsis = serializers.CharField(allow_blank=True, required=False)
    added_by = serializers.SerializerMethodField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def get_added_by(self, objCreate):
        added_by = objCreate.user.email
        return added_by


class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    movies_orders = MoviesSerializer(required=False, write_only=True)
    users_ordes = UserSerializer(required=False, write_only=True)
    buyed_at = serializers.DateTimeField(read_only=True)
    buyed_by = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    price = serializers.DecimalField(decimal_places=2, max_digits=8)

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)
    
    def get_buyed_by(self, objCreate):
        buyed_by = objCreate.users_ordes.email
        return buyed_by
    
    def get_title(self, objCreate):
        title = objCreate.movies_orders.title
        return title

