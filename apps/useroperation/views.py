from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
# Create your views here.

from .models import UserFav,UserLeavingMessafe,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,LeavingMessageSerializer
from .serializers import AddressSerializer
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
      展示用户收藏
    create:
      添加商品到用户收藏
    delete:
      删除用户收藏
    """
    serializer_class = UserFavSerializer
    permission_classes =(IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance=serializer.save()
        goods=instance.goods
        goods.fav_num+=1
        goods.save()
    def perform_destroy(self, instance):
        goods=instance.goods
        goods.fav_num-=1
        goods.save()
        instance.delete()
    def get_serializer_class(self):
        if self.action=="list":
            return UserFavDetailSerializer
        if self.action=="create":
            return UserFavSerializer

class LeavingMessageViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = LeavingMessageSerializer
    def get_queryset(self):
        return UserLeavingMessafe.objects.filter(user=self.request.user)

class AddressViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = AddressSerializer
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
