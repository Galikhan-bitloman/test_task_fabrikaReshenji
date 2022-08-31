from django.contrib import admin

from .models import Mailings, Client, Message

admin.site.register(Mailings)
admin.site.register(Client)
admin.site.register(Message)