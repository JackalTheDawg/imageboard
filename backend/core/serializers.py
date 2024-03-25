from rest_framework import serializers
from .models import *

class ProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
                "user_id",
                "name",
                "surname",
                "gender",
                "birthday",
                "profile_picture",
            )

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = (
            'id',
            'name',
            'description',
            'image',
            'private',
            'followers'
        )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'sender',
            'text',
            'content',
            'date',
            'mime',
            'location',
        )

class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            'sender',
            'post',
            'text',
            'content',
            'date'
        )