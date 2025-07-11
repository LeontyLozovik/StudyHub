from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index
from django_countries.fields import CountryField

LEVEL_CHOICES = [
    ('starter_level','Starter level'),
    ('middle_level', 'Middle level'),
    ('advanced_level', 'Advanced level')
]

STATUS_CHOICE = [
    ('draft','Draft'),
    ('published', 'Published')
]

NOTE_CHOICE = [
    ('public', 'Public'),
    ('private', 'Private')
]

RATE_CHOICE = [
    ('one', 1),
    ('two', 2),
    ('three', 3),
    ('four', 4),
    ('five', 5)
]

NOTIFICATION_STATUS = [
    ('unreaded', 'Unreaded'),
    ('readed', 'Readed')
]

NOTIFICATION_TYPE = [
    ('new_lesson', 'New lesson'),
    ('end_course', 'End course'),
    ('answer', 'Note answer'),
    ('unknown', 'Unknown')
]


class UserProfile(AbstractUser):
    avatar = models.ImageField(
        upload_to='main/avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text='Download your avatar'
    )
    bio = models.TextField(blank=True, null=True)
    country = CountryField(blank_label='Choose your country', default='BY')

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'Users'
        verbose_name_plural = 'User'


class Course(models.Model):
    author = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, related_name='my_courses')
    course_name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=False, null=False)
    cover = models.ImageField(
        upload_to='main/covers/',
        blank=False,
        null=False,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text='Download course cover'
    )
    date_of_publication = models.DateField(auto_now_add=True, blank=False, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, blank=False, null=False)
    users = models.ManyToManyField(to=UserProfile, related_name='courses')

    class Meta:
        db_table = 'courses'
        verbose_name = 'Courses'
        verbose_name_plural = 'Course'
        ordering = ['id', '-date_of_publication']
        indexes = [Index(fields=['-date_of_publication'])]


class Lesson(models.Model):
    author = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, null=True, related_name='my_lessons')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='lessons')
    lesson_name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    video = models.FileField(upload_to='main/video/')

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Lessons'
        verbose_name_plural = 'Lesson'


class Note(models.Model):
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, related_name='notes_to_lesson')
    user = models.ForeignKey(to=UserProfile, on_delete=models.SET_NULL, related_name='user_notes', null=True)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True, blank=False, null=False)
    availability = models.CharField(max_length=20, choices=NOTE_CHOICE, default='private', blank=False, null=False)

    class Meta:
        db_table = 'notes'
        verbose_name = 'Notes'
        verbose_name_plural = 'Note'
        ordering = ['id', '-created_at']


class Progress(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='users_progresses')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='courses_progresses')
    precent_of_complete = models.DecimalField(
        blank=False,
        null=False,
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    last_activity = models.DateTimeField(auto_now=True, blank=False, null=False)

    class Meta:
        db_table = 'progresses'
        verbose_name = 'Progresses'
        verbose_name_plural = 'Progress'
        ordering = ['id', '-last_activity']



class Review(models.Model):
    user = models.ForeignKey(to=UserProfile,on_delete=models.CASCADE, related_name='user_reviews')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='course_reviews')
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICE, blank=False, null=False)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'Reviews'
        verbose_name_plural = 'Review'
        ordering = ['id', '-created_at']


class Notification(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notify_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE, blank=False, null=False)
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS, blank=False, null=False)

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notifications'
        verbose_name_plural = 'Notification'
