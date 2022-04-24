from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .models.profile import Profile


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_verified')
    list_filter = ('is_verified',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    list_filter = ('created', )


