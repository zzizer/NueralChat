from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),
    path('chat/', views.new_chat, name='new_chat'),
     path('chat/<uuid:chat_id>/', views.chat_details, name='chat_details'),
    path('chat_reply/<uuid:id>/', views.chat_reply, name='chat_reply'),
]