from django.contrib import admin
from .models import Client, Request, Rating, News, Request2

#Register your models here
admin.site.register(Client)
admin.site.register(Request)
admin.site.register(Request2)
admin.site.register(Rating)
admin.site.register(News)