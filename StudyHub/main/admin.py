from django.contrib import admin

from .models import UserProfile, Course, Lesson, Note, Progress, Review, Notification

# Register your models here.

@admin.register(UserProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email', 'bio', 'country']
    list_filter = ['country']
    search_fields = ['pk', 'username', 'email']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
   list_display = ['pk', 'author', 'course_name', 'description', 'level', 'status', 'date_of_publication']
   list_filter = ['author', 'level', 'status']
   search_fields = ['pk', 'author', 'course_name', 'date_of_publication']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
   list_display = ['pk', 'lesson_name', 'description']
   list_filter = ['course']
   search_fields = ['pk', 'lesson_name']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'lesson', 'user', 'content', 'created_at', 'availability']
    list_filter = ['lesson', 'user', 'created_at', 'availability']
    search_fields = ['pk', 'lesson', 'user', 'created_at']


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'course', 'precent_of_complete']
    list_filter = ['user', 'course']
    search_fields = ['pk', 'user', 'course']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'course', 'rate', 'comment', 'created_at']
    list_filter = ['user', 'course', 'rate', 'created_at']
    search_fields = ['pk', 'user', 'course', 'created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'notify_type', 'status']
    list_filter = ['user', 'notify_type', 'status']
    search_fields = ['pk', 'user']
