from django.urls import path
from .views import ChatView, MessageView

urlpatterns = [
    path('', ChatView.as_view(), name='auth'),
    path('message/', MessageView.as_view(), name='auth')
]
