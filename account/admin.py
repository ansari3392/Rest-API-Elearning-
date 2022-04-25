from django.contrib import admin
from .models import CustomUser
from .models.profile import Profile


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'is_verified')
    list_filter = ('is_verified',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_teacher', 'is_consultant')
    list_filter = ('created', 'is_teacher', 'is_consultant')


