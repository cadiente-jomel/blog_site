from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from core.models import Comment, Profile
from django.contrib.auth.models import User


class CommentSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username', read_only=True)
    user_profile = serializers.SerializerMethodField()
    post = serializers.ReadOnlyField(source='post.title')
    created = serializers.ReadOnlyField()

    def get_user_profile(self, obj):
        u = User.objects.get(username=obj.user)
        return u.profile_img.profile.url

    # def create(self, validated_data):
    #     data = Profile.objects.get(user=user)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'post', 'user',  'created', 'user_profile']
