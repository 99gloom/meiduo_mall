from ronglian_sms_sdk import SmsSDK
from .constants import SEND_SMS_CODE_SEND_EXPIRES
from ..main import celery_app

sdk = SmsSDK(
    accId='2c94811c8a27cf2d018a4fbf69820f1b',
    accToken='11ad5611b8b94ba19f9cec65ee6de301',
    appId='2c94811c8a27cf2d018a4fbf6ad30f22',
)

@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):

    sdk.sendMessage('1', mobile, (sms_code, SEND_SMS_CODE_SEND_EXPIRES // 60))
