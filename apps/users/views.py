from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import mixins,viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
# Create your views here.

from random import choice

from .serializers import SmsSerializer,UserRegisterSerializer,UserDetailSerializer
from utils.yunpian import Yunpian
from mxshop.settings import APIKEY
from .models import VeifyCode
from .serializers import SmsSerializer

User=get_user_model()

class SmsCodeViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """create:
               发送验证码
               """
    serializer_class = SmsSerializer
    def generate_code(self):
        seeds="1234567890"
        code_dict=[]
        for i in range(4):
            code_dict.append(choice(seeds))
        return "".join(code_dict)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #获取验证通过的手机号
        mobile=serializer.validated_data["mobile"]

        code=self.generate_code()

        sms_yun=Yunpian(APIKEY)

        msg=sms_yun.send_sms(mobile=mobile,code=code)
        if msg["code"]!=0:
            return Response({
                "mobile":msg["msg"]
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            verify_code=VeifyCode(mobile=mobile,code=code)
            verify_code.save()
            return Response({
                "mobile":mobile
            },status=status.HTTP_201_CREATED)

class UserRegisterViewSet(mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """用户注册"""
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (authentication.BasicAuthentication,)

    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []

        return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer

        return UserDetailSerializer
    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()