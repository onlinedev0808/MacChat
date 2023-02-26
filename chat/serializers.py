from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Message, GroupMessage, Room

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    # Invokes djangos built-in password hashing function
    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

    class Meta:
        model = User
        fields = ['username', 'password']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']

class GroupSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    room = serializers.SlugRelatedField(many=False, slug_field='room', queryset=Room.objects.all())

    class Meta:
        model = GroupMessage
        fields = ['sender', 'room', 'message', 'timestamp']

class RoomSerializer(serializers.ModelSerializer):
    room = serializers.SlugRelatedField(many=False, slug_field='room', queryset=Room.objects.all())

    class Meta:
        model = Room
        fields = ['room']