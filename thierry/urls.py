from django.urls import path, include
from . import views

urlpatterns = [
    path('thierry-register/', views.thierryRegister, name='thierry-register'),
    path('thierry-login/', views.thierryLogin, name='thierry-login'),
    path('thierry-update/', views.thierryUpdate, name='thierry-update'),
    path('thierry-detail/', views.thierryDetail, name='thierry-detail'),
    path('thierry-delete/', views.thierryDelete, name='thierry-delete'),
    path('password-reset/', views.passwordReset, name='password_reset'),
    path('password-reset-confirm/<uid>/<token>/',
          views.passwordResetConfirm, name='password_reset_confirm'),

    #news urls
    path('news-list/', views.newsList, name='news-list'),
    path('news-detail/<str:pk>/', views.newsDetail, name='news-detail'),
    path('news-create/', views.newsCreate, name='news-create'),
    path('news-update/<str:pk>/', views.newsUpdate, name='news-update'),
    path('news-delete/<str:pk>/', views.newsDelete, name='news-delete'),

    #faq urls
    path('clientfaq-list/', views.ClientFAQList, name='clientfaq-list'),
    path('clientfaq-detail/<str:pk>/', views.ClientFAQDetail, name='clientfaq-detail'),
    path('clientfaq-create/', views.ClientFAQCreate, name='clientfaq-create'),
    path('clientfaq-update/<str:pk>/', views.ClientFAQUpdate, name='clientfaq-update'),
    path('clientfaq-delete/<str:pk>/', views.ClientFAQDelete, name='clientfaq-delete'),

    #faq urls
    path('manfaq-list/', views.ManFAQList, name='manfaq-list'),
    path('manfaq-detail/<str:pk>/', views.ManFAQDetail, name='manfaq-detail'),
    path('manfaq-create/', views.ManFAQCreate, name='manfaq-create'),
    path('manfaq-update/<str:pk>/', views.ManFAQUpdate, name='manfaq-update'),
    path('manfaq-delete/<str:pk>/', views.ManFAQDelete, name='manfaq-delete'),

    #contact urls
    path('contact-list/', views.contactList, name='contact-list'),
    path('contact-detail/<str:pk>/', views.contactDetail, name='contact-detail'),
    path('contact-create/', views.contactCreate, name='contact-create'),
]