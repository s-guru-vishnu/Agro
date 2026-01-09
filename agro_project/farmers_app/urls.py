from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    path('fertilizers/', views.fertilizers_page, name='fertilizers_page'),
    path('machines/', views.machines_page, name='machines_page'),
    path('manpower/', views.manpower_page, name='manpower_page'),
    path('sellers/', views.sellers_page, name='sellers_page'),
    path('api/get-availability/', views.get_availability, name='get_availability'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]