from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('create/', CreateCourse.as_view(), name='create_course')
]
