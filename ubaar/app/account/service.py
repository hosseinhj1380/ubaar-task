from app.account.models import  User
from app.OTP.models import OTP
from . selector import user_info
from app.OTP.utils import send_sms
def send_otp_sms(phone):
    user = user_info(phone=phone)
    
    user_otp = OTP.objects.get_or_create(user=user)
    
    if user_otp.is_block():
        return False , user_otp.block_expired_at

    if user_otp.attempt > 3 :
        user_otp.block()
        return False , user_otp.block_expired_at
    
    message = f"this is your code{user_otp.sms_code}"
    if send_sms(sms_message=message,phone_number=user.phone):
        print(user_otp.sms_code)
        user_otp.increase_expired_time()
        
        return True , user_otp

    
def active_user(otp_id):
    otp_obj = OTP.objects.get(id=id)
    
    
    