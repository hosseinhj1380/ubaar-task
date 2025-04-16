from app.account.models import User
from django.db.transaction import atomic
from django.core.exceptions import ValidationError
from app.OTP.models import OTP
def is_signed_up(phone):
    try:
        user = User.objects.get(phone=phone)
        if user.login_with_otp:
            return False
        return True
            
    except:
        with atomic():
            user =User.objects.create(phone=phone)
        return False
     
def user_info(phone):
    try:
        return User.objects.get(phone=phone)
    except User.DoesNotExist:
        raise ValidationError("user not found ")
    



