from django.contrib import admin

from myapp.models import contact, users

# Register your models here.
admin.site.register(users)
admin.site.register(contact)