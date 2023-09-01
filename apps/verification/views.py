import random
import django_redis
from rest_framework.response import Response
from rest_framework.views import APIView
from ronglian_sms_sdk import SmsSDK

# Create your views here.
sdk = SmsSDK(
    accId='2c94811c8a27cf2d018a4fbf69820f1b',
    accToken='11ad5611b8b94ba19f9cec65ee6de301',
    appId='2c94811c8a27cf2d018a4fbf6ad30f22'
)

class SMSCodeView(APIView):
    def get(self, request, mobile):
        # 1, 生成验证码
        sms_code = '%04d' % random.randint(0,9999)

        # 2, 创建redis连接对象
        redis_connect = django_redis.get_redis_connection('verify_codes')

        # 3, 把验证码存储至redis
        redis_connect.setex(f'sms_{mobile}', 300, sms_code)

        # 4, 将验证码发送到荣联云通讯
        res = sdk.sendMessage('1', mobile, (sms_code, 5))

        # 5, 相应
        return Response({'message': 'to'})