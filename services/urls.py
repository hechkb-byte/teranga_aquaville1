from django.urls import path
from . import views

urlpatterns = [
    path('inclus/', views.services_inclus, name='services_inclus'),
    path('parc-aquatique/', views.parc_aquatique, name='parc_aquatique'),
    path('spa/', views.spa, name='spa'),
    path('restauration/', views.restauration, name='restauration'),
]
