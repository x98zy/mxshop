from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

import re
import pytz
from datetime import datetime,timedelta

from mxshop.settings import REGEX_MOBILE
from .models import VeifyCode

User=get_user_model()
class SmsSerializer(serializers.Serializer):
    mobile=serializers.CharField(max_length=11)
    def validate_mobile(self, mobile):
        #验证手机号码是否被注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号码已被注册")

        #验证手机号码是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError("该手机号码非法")

        #验证验证码发送时间
        one_minute_ago=datetime.now()-timedelta(hours=0,minutes=1,seconds=0)
        if VeifyCode.objects.filter(add_time__gt=one_minute_ago,mobile=mobile).count():
            raise serializers.ValidationError("距离上次发送未超过一分钟")

        return mobile

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    class Meta:
        model = User
        fields = ("username", "gender", "birthday", "email", "mobile")

class UserRegisterSerializer(serializers.ModelSerializer):
    """用户手机注册Serializer"""
    code=serializers.CharField(required=True,max_length=4,min_length=4,
                               write_only=True,help_text="验证码",error_messages={
        "blank":"请输入验证码",
        "max_length":"验证码格式错误",
        "min_length": "验证码格式错误",
    })
    password=serializers.CharField(style={"input_type":"password"},write_only=True,help_text="密码")
    username=serializers.CharField(required=True,allow_blank=True,max_length=50,help_text="用户名",
                                   validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在")])
    mobile=serializers.CharField(required=True,allow_blank=True,max_length=11,min_length=11,help_text="手机号码")
    def create(self, validated_data):
        user=super().create(validated_data=validated_data)
        user.set_password(raw_password=validated_data["password"])
        user.save()
        return user
    def validate_code(self, code):

        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)#验证码有效期为5分钟
        #initial_data是前端所传递过来的数据
        code_records=VeifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        last_record=code_records[0]
        if last_record:
            if last_record.add_time>five_minute_ago.replace(tzinfo=pytz.timezone("UTC")):
                raise serializers.ValidationError("验证码过期")
            if last_record.code!=code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        """attrs作用于所有字段，他是validate_code等方法所返回的全部字段"""
        del attrs["code"]
        return attrs
    class Meta:
        model=User
        fields=["username","code","mobile","password"]