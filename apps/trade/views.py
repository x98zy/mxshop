from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication

from .serializers import ShopingCartSerializer,OrderSerializer
from .models import ShoppingCart,OrderInfo,OrderGoods

from utils.permissions import IsOwnerOrReadOnly
# Create your views here.

class ShopCartViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class = ShopingCartSerializer
    authentication_classes = (BasicAuthentication,SessionAuthentication)
    lookup_field = "goods_id"
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        instance=serializer.save()
        goods=instance.goods
        goods.goods_num-=instance.nums
        goods.save()
    def perform_update(self, serializer):
        existed_cart=ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums=existed_cart.nums
        save_record=serializer.save()
        save_nums=save_record.nums
        goods=save_record.goods
        nums_change=save_nums-existed_nums
        goods.goods_num-=nums_change
        goods.save()
    def perform_destroy(self, instance):
        goods=instance.goods
        goods.goods_num+=instance.nums
        goods.save()
        instance.delete()

class OrderViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class =OrderSerializer
    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order=serializer.save()
        shopcart_goods=ShoppingCart.objects.filter(user=self.request.user)
        for goods in shopcart_goods:
            order_goods=OrderGoods()
            order_goods.order=order
            order_goods.goods=goods.goods
            order_goods.goods_num=goods.nums
            order_goods.save()
            goods.delete()
        return order

