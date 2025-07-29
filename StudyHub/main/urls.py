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
    path('profile/<int:pk>/', Profile.as_view(), name='profile'),
    path('course/update/<int:pk>/', UpdateCourse.as_view(), name='update_course'),
    path('course/delete/<int:pk>/', DeleteCourse.as_view(), name='delete_course'),
    path('lesson/update/<int:pk>/', UpdateLesson.as_view(), name='update_lesson'),
    path('lesson/delete/<int:pk>/', DeleteLesson.as_view(), name='delete_lesson'),
    path('course/change_status/<int:pk>', change_status, name ='change_status'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('search/', Search.as_view(), name='search'),
    path('favorites/', Favorites.as_view(), name='favorites'),
    path('favorietes/change_state/<int:pk>/', fav_status_change, name='fav_change'),
    path('course/finish/', Feedback.as_view(), name='finish'),
    path('lesson/<int:pk>/create_note/', create_note, name='create_note'),
    path('lesson/note/update/<int:pk>', update_note, name='update_note'),
    path('lesson/note/delete/<int:pk>', DeleteNote.as_view(), name='delete_note'),
    path('lesson/<int:pk>/add_to_course/', add_to_course, name='add_lesson_to_course'),
    path('course/<int:pk>/start', StartCourse.as_view(), name='start_course'),
    path('course/<int:pk>/flip/', FlipPage.as_view(), name = 'flip'),
    path('course/<int:course_pk>/lesson/<int:lesson_pk>/done/', LessonDone.as_view(), name='lesson_done'),
    path('my_courses/', MyCourses.as_view(), name='my_courses')
]