import string
import random

from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password
from wall.models import BaseModel


class Writer(BaseModel):

    username = models.CharField(max_length=128, null=False, unique=True)
    name = models.CharField(max_length=128, null=False)
    email = models.CharField(max_length=128, null=False, unique=True)
    phone = models.CharField(max_length=32)
    password = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = "wall"
        db_table = "writer"

    def save(self, *args, **kwargs):
        super(Writer, self).save(*args, **kwargs)

    @staticmethod
    def create_random_password(size=5, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def encrypt_password(password):
        return make_password(password, settings.SECRET_KEY)

    @staticmethod
    def get_user_by_email_password(email, password=None):
        try:
            password = make_password(password, settings.SECRET_KEY)
            user = Writer.objects.get(email=email, password=password)
            return user
        except Writer.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_username_password(username, password=None):
        try:
            password = make_password(password, settings.SECRET_KEY)
            user = Writer.objects.get(username=username, password=password)
            return user
        except Writer.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_session(session_id):
        try:
            user = Session.objects.get(code=session_id)
            return user.writer
        except Session.DoesNotExist:
            return None


class EmailValidation(BaseModel):
    writer = models.ForeignKey(Writer, related_name='user_email_verification', on_delete=models.CASCADE)
    code = models.CharField(max_length=4, null=False)

    class Meta:
        app_label = "wall"
        db_table = "email_verification"


class Session(BaseModel):
    writer = models.ForeignKey(Writer, related_name='user_session', on_delete=models.CASCADE)
    code = models.CharField(max_length=36, null=False, primary_key=True)

    class Meta:
        app_label = "wall"
        db_table = "session"
