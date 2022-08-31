from rest_framework import serializers

from .models import Mailings, Client, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MailingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailings
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'