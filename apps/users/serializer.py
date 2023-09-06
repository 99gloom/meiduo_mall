import re

import django_redis
from rest_framework import serializers
from .models import User
from rest_framework_jwt.settings import api_settings

class CreateUserSerializer(serializers.ModelSerializer):

    # 序列化器的所有字段: ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 需要校验的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 模型中已存在的字段: ['id', 'username', 'password', 'mobile']
    # 需要序列化的字段: ['id', 'username', 'mobile', 'token']
    # 需要反序列化的字段: ['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']

    # 定义单向字段
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
        # 对字段增加额外约束
        extra_kwargs = {
            'username':{
                'min_length': 5,
                'max_length': 10,
                'error_messages':{
                    'min_length':'仅允许5-20个字符的用户名',
                    'max_length':'仅允许5-20个字符的用户名',
                }
            },
           'password': {
               'write_only': True,
               'min_length': 8,
               'max_length': 20,
               'error_messages': {
                   'min_length': '仅允许8-20个字符的用户名',
                   'max_length': '仅允许8-20个字符的用户名',
               }
           },
        }

    # 验证
    def validate_mobile(self, value):
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机格式错误')
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('手机号不一致')

        redis_connect = django_redis.get_redis_connection('verify_codes')
        redis_sms_code= redis_connect.get(f'sms_{attrs["mobile"]}')

        if not redis_sms_code or attrs['sms_code'] != redis_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        return attrs

    def create(self, validate_data):
        del validate_data['password2']
        del validate_data['sms_code']
        del validate_data['allow']
        password = validate_data.pop('password')
        user = User(**validate_data)
        user.set_password(password)
        user.save()



        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user







