from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav,UserLeavingMessafe
from .models import UserAddress


from goods.serializers import GoodsSerializers

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods=GoodsSerializers()
    class Meta:
        model=UserFav
        fields=("goods","id")

class UserFavSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=['user', 'goods'],
                message="该商品已经收藏"
            )
        ]
        model=UserFav
        fields=["user","goods","id"]

class LeavingMessageSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time=serializers.DateTimeField(read_only=True)
    class Meta:
        model=UserLeavingMessafe
        fields="__all__"

class AddressSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time=serializers.DateTimeField(read_only=True,format="%Y-%m-%d-%H:%M")
    class Meta:
        model=UserAddress
        fields=("user","address","signer_name","signer_mobile","province","city","add_time")