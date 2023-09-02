import random
import django_redis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ronglian_sms_sdk import SmsSDK
from .constants import SEND_SMS_CODE_SEND_EXPIRES, REDIS_SMS_CODE_EXPIRES
# Create your views here.
sdk = SmsSDK(
    accId='2c94811c8a27cf2d018a4fbf69820f1b',
    accToken='11ad5611b8b94ba19f9cec65ee6de301',
    appId='2c94811c8a27cf2d018a4fbf6ad30f22'
)

class SMSCodeView(APIView):
    def get(self, request, mobile):
        code_signal = f'sms_{mobile}'
        send_signal = f'send_{mobile}'

        # 0, 创建redis连接对象
        redis_connect = django_redis.get_redis_connection('verify_codes')

        # 1, 手机号是否近期已发送过短信
        send_flag = redis_connect.get(send_signal)
        if send_flag:
            return Response({
                'message':'发送过于频繁',
                status:status.HTTP_400_BAD_REQUEST
            })

        # 2, 生成验证码
        sms_code = '%04d' % random.randint(0,9999)

        # 3, 把验证码存储至redis
        # 3.1 创建管道，优化redis
        pl = redis_connect.pipeline()
        pl.setex(code_signal, REDIS_SMS_CODE_EXPIRES, sms_code)
        pl.setex(send_signal, SEND_SMS_CODE_SEND_EXPIRES, 1)
        pl.execute()

        # 4, 将验证码发送到荣联云通讯
        res = sdk.sendMessage('1', mobile, (sms_code, REDIS_SMS_CODE_EXPIRES // 60))

        # 5, 相应
        return Response({'message': 'to'})