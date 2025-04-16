from django.db.models import CharField,UUIDField,Model,DateTimeField,BooleanField,ForeignKey,CASCADE,IntegerField
from django.contrib.auth.base_user import AbstractBaseUser
from app.account.v1.validators import check_phone
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import timedelta




class Block(Model):
    attempt = IntegerField(default=0)
    blocked_at = DateTimeField(null=True, blank=True)
    block_expired_at = DateTimeField(null=True,blank=True)
    blocked = BooleanField(default=False)
    
    
    def is_block(self):
        if self.blocked:
            if timezone.now() > self.block_expired_at:
                return True
            self.attempt = 0 
            self.blocked = False
            self.blocked_at = None
            self.block_expired_at = None
            self.save()
        return False
    
    def block(self):
        self.blocked = True
        self.blocked_at = timezone.now()
        self.block_expired_at = timezone.now() + timedelta(hours=1)
        self.save()
        
    def attempt_inc(self):
        self.attempt +=1 
        self.save()
        

class User(AbstractBaseUser,Block):
    id = UUIDField(unique=True, db_index=True)
    password = CharField(_("password"), max_length=128,null=True)
    phone = CharField('phone number', max_length=11, null=True,unique=True, validators=[check_phone])
    first_name = CharField('first_name', max_length=200,default="")
    last_name = CharField('last_name', max_length=200,default="")
    is_new=BooleanField(default=True)
    login_with_otp = BooleanField(default=True)
    is_active = BooleanField(default=False)

    
    USERNAME_FIELD = 'phone'
    
