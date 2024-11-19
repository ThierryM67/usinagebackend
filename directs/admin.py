from django.contrib import admin
from .models import ManufacturerMessage, ClientMessage

# Register your models here.
admin.site.register(ManufacturerMessage)
admin.site.register(ClientMessage)