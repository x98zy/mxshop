"""mxshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token


from .settings import MEDIA_ROOT
from goods.view_base import GoodsListViewSet,GoodsCategoryViewSet,BananerViewset,IndexGategoryViewset
from users.views import SmsCodeViewSet,UserRegisterViewSet
from useroperation.views import UserFavViewSet,LeavingMessageViewset,AddressViewset
from trade.views import ShopCartViewset,OrderViewset

router=routers.DefaultRouter()
#配置goods路由
router.register("goods",GoodsListViewSet,basename="goods")
#配置category路由
router.register("categorys",GoodsCategoryViewSet,basename="categorys")
#配置短信验证码接口
router.register("code",SmsCodeViewSet,basename="code")
#配置用户注册
router.register("user",UserRegisterViewSet,basename="user")
#配置用户收藏
router.register("fav",UserFavViewSet,basename="fav")
#配置用户留言
router.register("message",LeavingMessageViewset,basename="message")
#配置用户收货地址
router.register("address",AddressViewset,basename="address")
#配置购物车
router.register("shopcart",ShopCartViewset,basename="shopcart")
#配置订单
router.register("orders",OrderViewset,basename="orders")
#配置轮播图
router.register("bananer",BananerViewset,basename="bananer")
#配置首页商品种类
router.register("indexcategory",IndexGategoryViewset,basename="indexcategory")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include(("rest_framework.urls","rest_framework"),namespace="api-auth")),
    re_path("media/(?P<path>.*)", serve, {'document_root': MEDIA_ROOT}),
    path("",include(router.urls)),
    path("docs/",include_docs_urls(title="生鲜商城")),

    #dr自带的token认证
    path("api-auth-token",views.obtain_auth_token),

    #jwt的token认证
    path("jwt-auth",obtain_jwt_token),
    #第三方登录
    path('', include(('social_django.urls','social_django'), namespace='social'))
]
