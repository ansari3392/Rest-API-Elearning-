from django.contrib import admin
from .models.course import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_filter = ('created', )


