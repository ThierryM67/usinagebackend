from django.contrib import admin
from .models import Contact, News, ClientFAQ, ManFAQ, Admin

# Register your models here.
admin.site.register(News)
admin.site.register(ClientFAQ)
admin.site.register(ManFAQ)
admin.site.register(Contact)
admin.site.register(Admin)