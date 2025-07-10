from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('lessons/', Lessons.as_view(), name='lessons'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('create/course/', CreateCourse.as_view(), name='create_course'),
    path('course/<int:pk>/', OneCourse.as_view(), name='one_course'),
    path('create/lesson/', CreateLesson.as_view(), name='create_lesson'),
    path('lesson/<int:pk>/', OneLesson.as_view(), name='one_lesson'),
    path('profile/<int:pk>', Profile.as_view(), name='profile')
]