from django.urls import path

from emailer import views

urlpatterns = [
    path('', views.send),
    path('sent', views.sent),
    path('error', views.exception)
]