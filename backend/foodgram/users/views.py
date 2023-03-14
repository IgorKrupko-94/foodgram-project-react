from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST
                                   )

from .models import Follow
from .serializers import FollowSerializer, CustomUserSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(detail=False)
    def subscriptions(self, request):
        follows = request.user.follower.all()
        pages = self.paginate_queryset(follows)
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            serializer = FollowSerializer(author, data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            Follow.objects.create(
                user=self.request.user,
                author=author
            )
            return Response(serializer.data, status=HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=self.request.user, author=author)
        follow.delete()
        return Response(status=HTTP_204_NO_CONTENT)
