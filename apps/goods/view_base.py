from django.views.generic import View
from django.http import HttpResponse
from django.core import serializers
from rest_framework import mixins
from rest_framework import generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
import json

from .models import Goods,GoodsCategory,Bananer
from .filters import GoodsFilter
from .serializers import GoodsSerializers,GoodsCategorySerializer,BananerSerializer,IndexCategotySerializer


class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """list:
         展示所有商品
       retrieve:
         获取商品详情"""
    throttle_classes = (AnonRateThrottle,UserRateThrottle)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializers
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class=GoodsFilter
    search_fields = ['goods_desc', 'goods_brief',"name"]
    ordering_fields = ['click_num', 'sold_num']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num+=1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GoodsCategoryViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
      展示商品分类
    retrieve:
      获取具体商品分类详情
    """
    throttle_classes = (AnonRateThrottle, UserRateThrottle)
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = GoodsCategorySerializer

class BananerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """list:
       展示商品轮播图"""
    queryset = Bananer.objects.all().order_by("index")
    serializer_class = BananerSerializer

class IndexGategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_table=True)
    serializer_class = IndexCategotySerializer