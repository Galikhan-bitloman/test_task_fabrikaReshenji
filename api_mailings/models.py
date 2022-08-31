from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

import pytz
import uuid


class Mailings(models.Model):
    mailings_id = models.UUIDField(verbose_name='Mailing\'s id', default=uuid.uuid4())
    start_date = models.DateField(verbose_name='Starting date to mail')
    start_time = models.TimeField(verbose_name="Starting time to mail")
    end_date = models.DateField(verbose_name='End of date to mail')
    end_time = models.TimeField(verbose_name='End of time to mail')
    tag = models.CharField(max_length=20, verbose_name='Client\'s tag', null=True)
    mobile_operator_code_mailing = models.CharField(max_length=20, verbose_name='Client\'s mobile operator code', null=True)

    def __str__(self):
        return f'Mailing {self.mailings_id} time - {self.start_date}, {self.end_time}'




class Client(models.Model):
    phone_regex = RegexValidator(regex=r'^7\d{10}$',
                                 message="The client's phone number in the format 7XXXXXXXXXX (X - number from 0 to 9)")
    USERS_TIMEZONE = (
        tuple(zip(pytz.all_timezones, pytz.all_timezones))
    )

    client_id = models.UUIDField(verbose_name='Client\'s id', default=uuid.uuid4())
    phone_number = models.CharField(max_length=11, verbose_name='Client\'s phone number', validators=[phone_regex], unique=True)
    mobile_operator_code_client = models.CharField(max_length=4, verbose_name='Mobile operator code', editable=False)
    tag = models.CharField(max_length=20, verbose_name='Tag')
    time_zone = models.CharField(max_length=32, verbose_name='Timezone', choices=USERS_TIMEZONE, default='Asia/Almaty')

    def save(self, *args, **kwargs):
        self.mobile_operator_code_client = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f'Client {self.client_id} with phone number {self.phone_number}'

class Message(models.Model):
    SHIPPING = (
       ('Sent', 'sent'),
        ('Didn\'t sent', 'didn\'t sent'),
    )
    message_id = models.UUIDField(verbose_name='Message\'s id', default=uuid.uuid4())
    date_of_sending = models.DateField(verbose_name='Date of sending')
    time_of_sending = models.TimeField(verbose_name='Time of sending')
    status_of_shipping = models.CharField(max_length=11, verbose_name='Status of shipping', choices=SHIPPING)
    mailing = models.ForeignKey(Mailings, on_delete=models.CASCADE, related_name='message_mailing')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='message_client')


    def __str__(self):
        return f'Message: Client - {self.client}, Mailing - {self.mailing}'

