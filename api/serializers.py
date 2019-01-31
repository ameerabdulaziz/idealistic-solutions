from rest_framework import serializers
# from posts import models
from django.contrib.auth import get_user_model


# If you want to use url in details use below and call 'url' in fields
# class PostsSerializers(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="api:posts")
    # user = UserSerializer()
# class PostsSerializers(serializers.ModelSerializer):
#     class Meta:
#         Call table you want from models
#         model = models.Post
#         Call fields you want from this table
#         fields = ('user', 'category', 'title', 'slug', 'content', 'main_image', 'images', 'created_date', 'updated_date')
