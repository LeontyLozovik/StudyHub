from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('signup', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('create/', CreateCourse.as_view(), name='create_course')
]