from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField




class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('User must have a phone number')
        if not password:
            raise ValueError('User must have a password')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_admin = False
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        user = self.create_user(phone, password=password, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Vendor(AbstractBaseUser):
    vendor_code = models.UUIDField(
        verbose_name=_('vendor_code'),
        unique=True,
        help_text=_('Required. A 32 hexadecimal digits number as specified in RFC 4122.'),
        error_messages={
            'unique': _('A vendor with that vendor_code already exists.'),
        },
        default=uuid.uuid4,
    )
    phone = PhoneNumberField(_('contact details'), null=True, blank=True, unique=True,
                             error_messages={'unique': _('A vendor with that phone already exists.')}, )

    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    address = models.TextField(_('address'), max_length=500, blank=True, null=True)
    on_time_delivery_rate = models.FloatField(_('on time delivery rate'), blank=True, null=True)
    quality_rating_avg = models.FloatField(_('quality rating avg'), blank=True, null=True)
    average_response_time = models.FloatField(_('average response time'), blank=True, null=True)
    fulfillment_rate = models.FloatField(_('fulfillment rate'), blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    first_login = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone


class HistoricalPerformance(TimeStampedModel):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = _('Historical Performance')
        verbose_name_plural = _('Historical Performances')

    def __str__(self):
        return f"{self.vendor} - {self.date}"
