from rest_framework.serializers import Serializer,ModelSerializer,CharField,IntegerField,DictField,UUIDField,ValidationError
from .validators import check_phone , check_sms_code
from django.conf import settings
from app.OTP.models import OTP
class ResponseBaseClass(Serializer):
    message = CharField(required=False)
    data = DictField(required=True)

    class Meta:
        ref_name = "ResponseBaseClass"



class LoginSerializer(Serializer):
    phone = CharField(required = True,validators=[check_phone])
    
class OTPResponseSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = ("id","created_at","expired_at","user__login_with_otp")
    
class VerifyOTPSerializer(Serializer):
    id = UUIDField(required = True)
    sms_code = CharField(required = True,validators=[check_sms_code])

    def validate(self, attrs):
        try:
            otp_obj = OTP.objects.get(id=attrs["id"])
        except OTP.DoesNotExist:
            raise ValidationError("OTP not found.")

        if otp_obj.sms_code != attrs["sms_code"]:
            raise ValidationError("Invalid OTP.")
        if not otp_obj.is_expired():
            raise ValidationError("OTP expired.")
        
        return attrs
    


# class LoginResponseSerializer(ResponseBaseClass):
#     class info(ModelSerializer):
#         class Meta:
#             model = settings.AUTH_USER_MODEL
            
#             field = ("")