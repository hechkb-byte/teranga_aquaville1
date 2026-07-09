from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('villas/vente/', views.villas_vente, name='villas_vente'),
    path('villas/vente/<slug:slug>/', views.villa_detail_vente, name='villa_detail_vente'),
    path('villas/location/', views.villas_location, name='villas_location'),
]
