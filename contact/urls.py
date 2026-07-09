from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('merci/', views.contact_succes, name='contact_succes'),
]
