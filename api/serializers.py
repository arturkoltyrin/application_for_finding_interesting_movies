from rest_framework import serializers

from interactions.models import Interaction
from movies.models import Actor, Genre, Movie
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    preferred_genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "email", "avatar", "preferred_genres"]


class InteractionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Interaction
        fields = ["id", "rating", "movie", "user", "timestamp"]
        read_only_fields = ["user", "timestamp"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "avatar")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "avatar", "preferred_genres"]
        extra_kwargs = {
            "email": {"required": False},
            "password": {"required": False},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("")
        return value


class PageRankRecommendationSerializer(serializers.Serializer):
    movie = MovieSerializer()
    score = serializers.FloatField()


class CollaborativeRecommendationSerializer(serializers.Serializer):
    movie = MovieSerializer()
    predicted_rating = serializers.FloatField()
