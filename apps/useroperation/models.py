from django.db import models
from django.contrib.auth import get_user_model


from goods.models import Goods
# Create your models here.


User=get_user_model()


class UserFav(models.Model):
    """
    用户收藏
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品",help_text="收藏商品")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        unique_together=("user","goods")
    def __str__(self):
        return self.user.name


class UserLeavingMessafe(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES=(
        (1,"留言"),
        (2,'投诉'),
        (3,'询问'),
        (4,'求购'),
        (5,'售后'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_type=models.IntegerField(default=1,choices=MESSAGE_CHOICES,verbose_name="留言类型")
    subject=models.CharField(max_length=100,verbose_name="主题")
    message=models.TextField(verbose_name="留言")
    file=models.FileField(verbose_name="上传文件")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.subject

class UserAddress(models.Model):
    """用户地址"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    address=models.CharField(max_length=200,verbose_name="详细地址")
    signer_name=models.CharField(max_length=100,verbose_name="签收人")
    signer_mobile=models.CharField(max_length=100,verbose_name="签收电话")
    province = models.CharField(max_length=200,default="", verbose_name="省份")
    city = models.CharField(max_length=200, default="",verbose_name="城市")
    district=models.CharField(max_length=200,verbose_name="区域")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address