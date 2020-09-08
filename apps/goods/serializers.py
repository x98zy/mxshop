from rest_framework import serializers
from django.db.models import Q

from .models import Goods,GoodsCategory,GoodsImage,Bananer,GoodsCategoryBrand


class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat=GoodsCategorySerializer3(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat=GoodsCategorySerializer2(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsImage
        fields=("images",)
class GoodsSerializers(serializers.ModelSerializer):
    category=GoodsCategorySerializer()
    images=GoodsImageSerializer(many=True)
    class Meta:
        model=Goods
        fields="__all__"

class BananerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bananer
        fields="__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

class IndexCategotySerializer(serializers.ModelSerializer):
    brands=BrandSerializer(many=True)
    goods=serializers.SerializerMethodField()
    sub_cat=GoodsCategorySerializer2(many=True)

    def get_goods(self,obj):
        all_goods=Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer=GoodsSerializers(all_goods,many=True,context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model=GoodsCategory
        fields="__all__"