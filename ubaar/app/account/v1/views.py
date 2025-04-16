from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import PhoneVerification, Blacklist
from .serializers import LoginSerializer,ResponseBaseClass,OTPResponseSerializer,VerifyOTPSerializer
from django.utils import timezone
from datetime import timedelta
import random
from app.account import selector , service
from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS,HTTP_200_OK
BLOCK_DURATION = timedelta(hours=1)


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone=serializer.validated_data["phone"]
        if selector.is_signed_up(phone):
            return self.password_login()
        else:
            return self.otp_login(phone=phone)
            
    def otp_login(self,phone):
        stat ,res = service.send_otp_sms(phone) 
        if stat: 
            return Response(
            ResponseBaseClass({"message":"user has been blocked","data":{"unblocked_at":res["block_expired_at"]}}).data,
                status=HTTP_429_TOO_MANY_REQUESTS,
            )
        
        return Response(
        OTPResponseSerializer(res).data,
            status=HTTP_200_OK,
        ) 
    
    def password_login(self,request):
        pass 
    
    
class VerifyOtp(APIView):
    def post(self,request):
        
        serializer = VerifyOTPSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        if service.active_user(serializer.validated_data["id"]):
            pass 
