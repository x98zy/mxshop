from rest_framework import viewsets
from rest_framework import serializers

import time,random

from goods.models import Goods
from .models import ShoppingCart,OrderInfo

class ShopingCartSerializer(serializers.Serializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums=serializers.IntegerField(required=True,label="数量",min_value=1,error_messages=
    {"required":"必填字段","min_value":"数量最小为1"})
    goods=serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user=self.context["request"].user
        nums=validated_data["nums"]
        goods=validated_data["goods"]

        existed=ShoppingCart.objects.filter(user=user,goods=goods)
        if existed:
            existed=existed[0]
            existed.nums+=nums
            existed.save()
        else:
            existed=ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums=validated_data["nums"]
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=OrderInfo
        fields="__all__"
    def generate_order(self):
        """生成随机订单编号"""
        randobj=random.Random()
        order_sn="{time}{userid}{randstr}".format(time=time.strftime("%Y%m%d%H%M%S"),userid=self.context["request"].user.id,
                                                   randstr=randobj.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"]=self.generate_order()
        return attrs