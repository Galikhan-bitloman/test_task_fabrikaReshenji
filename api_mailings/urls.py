from django.urls import path

from rest_framework import routers

from .views import ClientListView, ClientDetailView, MailingListView, MailingDetailView, MessageListView

router = routers.DefaultRouter()
router.register(r'client', ClientListView, basename='ClientList')
router.register(r'client-detail', ClientDetailView, basename='ClientDetail')
router.register(r'mailings', MailingListView, basename='MailingList')
router.register(r'mailings-detail', MailingDetailView, basename='MailingDetail')

# urlpatterns = [
#     path('client/', ClientListView.as_view()),
#     path('client-detail/<int:pk>', ClientDetailView.as_view()),
#     path('mailing/', MailingListView.as_view()),
#     path('mailing-detail/<int:pk>', MailingDetailView.as_view()),
#
# ]