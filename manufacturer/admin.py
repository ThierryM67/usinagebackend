from django.contrib import admin
from .models import Manufacturer, Offer, Rating

#Register your models here
admin.site.register(Manufacturer)
admin.site.register(Offer)
admin.site.register(Rating)
