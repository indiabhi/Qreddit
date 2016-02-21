from django.contrib import admin
from .models import Page,Category,UserProfile
# Register your models here.

admin.site.register(Page)
admin.site.register(Category)
admin.site.register(UserProfile)
