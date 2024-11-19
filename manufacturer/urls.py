from django.urls import path, include
from . import views

urlpatterns = [
    #manufacturer urls
    path('manufacturer-register/', views.manufacturerRegister, name='manufacturer-register'),
    path('manufacturer-login/', views.manufacturerLogin, name='manufacturer-login'),
    path('manufacturer-detail/', views.manufacturerDetail, name='manufacturer-detail'),
    path('manufacturer-detail/<str:pk>/', views.manufacturerDetail2, name='manufacturer-detail2'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('manufacturer-logout/', views.manufacturerLogout, name='manufacturer-logout'),
    path('manufacturer-update/<str:pk>/', views.manufacturerUpdate, name='manufacturer-update'),
    path('manufacturer-delete/<str:pk>/', views.manufacturerDelete, name='manufacturer-delete'),
    #manufacturer reset password
    path('password-reset/', views.passwordReset, name='password_reset'),
    path('password-reset-confirm/<uid>/<token>/',
          views.passwordResetConfirm, name='password_reset_confirm'),


    #offer urls
    path('general-offer-list/', views.generalOfferList, name='general-offer-list'),
    path('manufacturer-offer-list/<str:pk>/', views.manufacturerOfferList, name='manufacturer-offer-list'),
    path('request-offer-list/<str:pk>/', views.requestOfferList, name='request-offer-list'),
    path('offer-manufacturers/', views.offerManufs, name='offer-manufacturers'),
    path('manufacturer-request-list/<str:pk>/', views.manufacturerRequestList, name='manufacturer-request-list'),
    path('offer-detail/<str:pk>/', views.offerDetail, name='offer-detail'),
    path('offer-create/', views.offerCreate, name='offer-create'),
    path('offer-create2/', views.offerCreateb, name='offer-create2'),
    path('offer-update/<str:pk>/', views.offerUpdate, name='offer-update'),
    path('offer-delete/<str:pk>/', views.offerDelete, name='offer-delete'),
    
    #ratings urls
    path('manuf-rating-list/', views.ratingList, name='rating-list'),
    path('manuf-rating-detail/<str:pk>/', views.ratingDetail, name='rating-detail'),
    path('manufacturer-rating/<str:pk>/', views.manufacturerAverageRating, name='manufacturer-rating'),
    path('manuf-rating-create/', views.ratingCreate, name='rating-create'),
    path('manuf-rating-update/<str:pk>/', views.ratingUpdate, name='rating-update'),
    path('manuf-rating-delete/<str:pk>/', views.ratingDelete, name='rating-delete'),
]