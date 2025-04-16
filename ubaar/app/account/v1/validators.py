from django.core.exceptions import ValidationError

def check_phone(value):
    if not (value.isnumeric() and len(value) == 11 and value.startswith("09")):
        raise ValidationError("phone number is not valid ")
    
def check_sms_code(value):
    if len(value) != 6 :
        raise ValidationError("sms_code is not valid")
    
    