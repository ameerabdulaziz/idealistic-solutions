# from django.shortcuts import render
# from rest_framework import viewsets, permissions
# from .serializers import PostsSerializers
# from rest_framework.authentication import TokenAuthentication
# from posts import models
#
#
# def api_index(request):
#     message = 'Hello from API Home'
#     return render(request, 'index.html', context={"message":message,})
#
# class Posts_Api(viewsets.ModelViewSet):
#     queryset = models.Post.objects.all()
#     serializer_class = PostsSerializers
#     Create this line to prevent error "{"detail":"CSRF Failed: CSRF token missing or incorrect."}"
#     authentication_classes = (TokenAuthentication,)
#     TO add specifi permisions to one api.
#     permissions_classes = (permissions.IsAuthenticatedOrReadOnly)
