from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Userprofile(AbstractUser):
    """
    用户
    """
    name=models.CharField(max_length=100,null=True,blank=True,verbose_name='用户名')#null为True表示数据库可以为空，blank=True表示填写表单时可以为空
    birthday=models.DateField(null=True,blank=True,verbose_name="出生年月")
    mobile=models.CharField(max_length=11,verbose_name="电话号码",help_text="手机号")
    gender=models.CharField(max_length=10,choices=(("male","男"),("female","女")),default="female",verbose_name="性别")
    email=models.CharField(max_length=100,null=True,blank=True,verbose_name="电子邮件")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    class Meta:
        verbose_name="用户"
        verbose_name_plural="用户"
    def __str__(self):
        return self.username


class VeifyCode(models.Model):
    """
    短信验证码
    """
    code=models.CharField(max_length=10,verbose_name="短信验证码")
    mobile=models.CharField(null=True,blank=True,max_length=11,verbose_name="电话")
    add_time=models.DateTimeField(auto_now_add=True,verbose_name="添加时间")
    class Meta:
        verbose_name="短信验证码"
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.code