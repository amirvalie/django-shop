from django.contrib import admin
from .models import PhoneToken,User

# Register your models here.

admin.site.register(PhoneToken)
admin.site.register(User)