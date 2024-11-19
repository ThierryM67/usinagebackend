from django.urls import path, include
from . import views

urlpatterns = [
    path('manufacturer/', include('manufacturer.urls')),

    #client urls
    path('client-register/', views.clientRegister, name='client-register'),
    path('client-login/', views.clientLogin, name='client-login'),
    path('client-detail/', views.clientDetail, name='client-detail'),
    path('client-detail/<str:pk>/', views.clientDetail2, name='client-detail2'),
    path('clients/', views.clients, name='clients'),
    path('client-logout/', views.clientLogout, name='client-logout'),
    path('client-update/<str:pk>/', views.clientUpdate, name='client-update'),
    path('client-delete/<str:pk>/', views.clientDelete, name='client-delete'),
    #client reset password
    path('password-reset/', views.passwordReset, name='password_reset'),
    path('password-reset-confirm/<uid>/<token>/',
          views.passwordResetConfirm, name='password_reset_confirm'),

    #request urls
    path('general-request-list/', views.generalRequestList, name='general-request-list'),
    path('general-request-list2/', views.generalRequestList2, name='general-request-list2'),
    path('client-request-list/<str:pk>/', views.clientRequestList, name='client-request-list'),
    path('client-request-list2/<str:pk>/', views.clientRequestList2, name='client-request-list'),
    path('request-detail/<str:pk>/', views.requestDetail, name='request-detail'),
    path('request-detail2/<str:pk>/', views.requestDetail2, name='request-detail'),
    path('request-create/', views.requestCreate, name='request-create'),
    path('request-create2/', views.requestCreate2, name='request-create'),
    path('request-createb/', views.requestCreateb, name='request-create'),
    path('request-update/<str:pk>/', views.requestUpdate, name='request-update'),
    path('request-delete/<str:pk>/', views.requestDelete, name='request-delete'),
    
    #ratings urls
    path('rating-list/', views.ratingList, name='rating-list'),
    path('rating-detail/<str:pk>/', views.ratingDetail, name='rating-detail'),
    path('client-rating/<str:pk>/', views.clientAverageRating, name='client-rating'),
    path('rating-create/', views.ratingCreate, name='rating-create'),
    path('rating-update/<str:pk>/', views.ratingUpdate, name='rating-update'),
    path('rating-delete/<str:pk>/', views.ratingDelete, name='rating-delete'),
    
    #news urls
    path('news-list/', views.newsList, name='news-list'),
    path('news-detail/<str:pk>/', views.newsDetail, name='news-detail'),
    path('news-create/', views.newsCreate, name='news-create'),
    path('news-update/<str:pk>/', views.newsUpdate, name='news-update'),
    path('news-delete/<str:pk>/', views.newsDelete, name='news-delete'),


    path('webhooks/paypal/', views.Webhook, name='paypal')

    #path('paypal/create-order/', views.create_order, name='create_order'),
    #path('paypal/capture-order/<str:order_id>/', views.capture_order, name='capture_order'),
]