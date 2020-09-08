from django.contrib import admin


from .models import GoodsCategory,GoodsCategoryBrand,Goods,GoodsImage,Bananer
# Register your models here.

admin.site.register(GoodsCategory)
admin.site.register(GoodsCategoryBrand)
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(Bananer)
