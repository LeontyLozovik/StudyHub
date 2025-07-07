from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreateCourseForm, LoginForm, SignupForm
from .models import Course, UserProfile


# Create your views here.
class Login(LoginView):
    authentication_form  = LoginForm
    template_name = 'main/login.html'
    success_url = reverse_lazy('main_page')


class Signup(CreateView):
    model = UserProfile
    form_class = SignupForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('main_page')


class MainPage(ListView):
    model = Course
    template_name = 'main/main_page.html'
    context_object_name = 'courses'
    paginate_by = 8
    ordering = ['-date_of_publication']


class CreateCourse(CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'main/course_form.html'
    success_url = reverse_lazy('main_page')

