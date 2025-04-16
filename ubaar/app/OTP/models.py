from django.db import models
from django.db.models import CharField,UUIDField,Model,DateTimeField,BooleanField,ForeignKey,CASCADE
from django.contrib.auth.base_user import AbstractBaseUser
from app.account.v1.validators import check_phone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from app.account.models import Block
import random
from datetime import timedelta

class OTP(Block):
    user=ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    id = UUIDField(unique=True)
    created_at = DateTimeField(auto_now_add=True)
    expired_at = DateTimeField()
    sms_code = CharField(default=random.sample(range(1,101),6))
    code_validation = BooleanField(default=False)
    
    
    
    def is_expired(self):
        return timezone.now() > self.expired_at

    def increase_expired_time(self):
        self.expired_at =timezone.now() + timedelta(minutes=1)
        self.save()
