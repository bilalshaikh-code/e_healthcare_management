from typing import Any
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True


    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError ('email is require')
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    


    def  create_superuser(self,email,password=None,**extra_fields ):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('role',"admin")

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('super user must have is_staff true'))
        
        return self.create_user(email,password,**extra_fields)

        


# from django.core.mail import send_mail
# # import uuid
# from django.conf import settings

# from django.core.mail import send_mail
# from django.conf import settings

# def send_forget_password_mail(email, token):
#     subject = 'Password Reset Link'
#     message = f'Hi, please click the link below to reset your password:\n\n' \
#               f'http://127.0.0.1:8000/account1/change_password/{token}/'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     send_mail(subject, message, email_from, recipient_list)
#     return True
