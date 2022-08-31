from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .serializer import MailingsSerializer, ClientSerializer, MessageSerializer
from .models import Client, Mailings, Message


class ClientListView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get_object(self, pk):
        try:
            return Client.objects.get(id=pk)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        clients = self.get_object(pk)
        serializer = ClientSerializer(clients)
        return Response(serializer.data)

    def put(self, request, pk):
        clients = self.get_object(pk)
        serializer = ClientSerializer(data=request.data, instance=clients)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        clients = self.get_object(pk)
        clients.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MailingListView(viewsets.ModelViewSet):
    serializer_class = MailingsSerializer
    queryset = Mailings.objects.all()

    def get(self, request):
        mailings = Mailings.objects.all()
        serializer = MailingsSerializer(mailings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MailingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True)
    def stat_info(self, request, pk):
        queryset = Mailings.objects.all()
        get_object_or_404(queryset, pk=pk)
        queryset_message = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset_message, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def full_stat_info(self, request):

        total_count = Mailings.objects.count()
        mailing = Mailings.objects.values('id')
        content = {'Total number of mailings': total_count,
                   'The number of messages sent': ''}
        result = {}

        for row in mailing:
            res = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            sent = mail.filter(status_of_shipping='Sent').count()
            no_sent = mail.filter(status_of_shipping='No sent').count()
            res['Total messages'] = len(mail)
            res['Sent'] = sent
            res['No sent'] = no_sent
            result[row['id']] = res

        content['The number of messages sent'] = result
        return Response(content)


class MailingDetailView(viewsets.ModelViewSet):
    serializer_class = MailingsSerializer
    queryset = Mailings.objects.all()

    def get_object(self, pk):
        try:
            return Mailings.objects.get(id=pk)
        except Mailings.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        mailings = self.get_object(pk)
        serializer = MailingsSerializer(mailings)
        return Response(serializer.data)

    def put(self, request, pk):
        mailings = self.get_object(pk)
        serializer = MailingsSerializer(data=request.data, instance=mailings)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mailings = self.get_object(pk)
        mailings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def messageList(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)




