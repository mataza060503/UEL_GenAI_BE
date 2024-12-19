from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.prompt),
    path('chat/', views.chat)
]
