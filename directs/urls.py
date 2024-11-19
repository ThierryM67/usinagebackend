from django.urls import path
from . import views

urlpatterns = [
    #client urls
    path('client-unread/', views.clientUnread, name='client-unread'),
    path('client-inbox/', views.clientInbox, name='client-inbox'),
    path('client-chat/<str:pk>/', views.clientChat, name='client-chat'),
    path('client-send/', views.clientSend, name='client-logout'),

    
    #manufacturer urls
    path('manufacturer-unread/', views.manufacturerUnread, name='manufacturer-unread'),
    path('manufacturer-inbox/', views.manufacturerInbox, name='manufacturer-inbox'),
    path('manufacturer-chat/<str:pk>/', views.manufacturerChat, name='manufacturer-chat'),
    path('manufacturer-send/', views.manufSend, name='manufacturer-logout'),
    
]