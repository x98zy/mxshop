from django.db import models
from django.contrib.auth import get_user_model


from goods.models import Goods
# Create your models here.
User=get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    goods=models.ForeignKey(Goods,on_delete=models.CASCADE,verbose_name="商品")
    nums=models.IntegerField(default=0,verbose_name="商品数量")
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="购物车"
        verbose_name_plural=verbose_name
        unique_together=("user","goods")
    def __str__(self):
        return "%s(%d)"%(self.goods.name,self.goods_num)


class OrderInfo(models.Model):
    """
    订单详情
    """
    ORDER_STATUS=(
        ("success","成功"),
        ("cancel","取消"),
        ("waiting","待支付")
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="用户")
    order_sn=models.CharField(max_length=40,verbose_name="订单编号",null=True,blank=True)#订单编号
    trade_no=models.CharField(max_length=40,verbose_name="交易编号",null=True,blank=True)#交易编号
    pay_status=models.CharField(choices=ORDER_STATUS,max_length=30,verbose_name="支付状态")#支付状态
    order_mount=models.FloatField(default=0.0,verbose_name="支付金额")#支付金额
    post_script=models.CharField(max_length=300,verbose_name="订单留言")
    pay_time=models.DateTimeField(null=True,blank=True,verbose_name="支付时间")#支付时间
    address=models.CharField(max_length=30,default="",verbose_name="收获地址")#收货地址
    signer_name=models.CharField(max_length=30,verbose_name="签收人")#签收人姓名
    signer_mobile=models.CharField(max_length=30,verbose_name="联系电话")#签收人电话
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="订单"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.order_sn


class OrderGoods(models.Model):
    """
    订单的商品，一个订单可能有多个商品
    """
    order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE,verbose_name="订单",related_name="goods")
    goods= models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    goods_num=models.IntegerField(verbose_name="商品数量")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name="订单商品"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.order.order_sn