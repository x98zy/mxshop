from django.contrib import admin


from .models import UserFav,UserLeavingMessafe,UserAddress
# Register your models here.


admin.site.register(UserFav)
admin.site.register(UserLeavingMessafe)
admin.site.register(UserAddress)