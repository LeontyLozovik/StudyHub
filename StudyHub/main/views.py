from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CreateCourseForm, LoginForm, SignupForm, CreateLessonForm
from .models import Course, UserProfile, Lesson


# Create your views here.
class Login(LoginView):
    authentication_form  = LoginForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('main_page')


class Signup(CreateView):
    model = UserProfile
    form_class = SignupForm
    template_name = 'main/signup.html'
    success_url = reverse_lazy('main_page')


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')



class MainPage(ListView):
    model = Course
    template_name = 'main/main_page.html'
    context_object_name = 'courses'
    paginate_by = 8
    ordering = ['-date_of_publication']


class CreateCourse(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'main/course_form.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'draft'
        return super().form_valid(form)


class OneCourse(DetailView):
    model = Course
    template_name = 'main/one_course.html'
    context_object_name = 'course'


class CreateLesson(CreateView):
    model = Lesson
    form_class = CreateLessonForm
    template_name = 'main/create_lesson.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class Lessons(ListView):
    model = Lesson
    template_name = 'main/lessons.html'
    context_object_name = 'lessons'
    paginate_by = 8


class OneLesson(DetailView):
    model = Lesson
    template_name = 'main/one_lesson.html'
    context_object_name = 'lesson'


class Profile(DetailView):
    model = UserProfile
    template_name = 'main/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['published_courses'] = user.my_courses.filter(status='published').order_by('-date_of_publication')
        context['draft_courses'] = user.my_courses.filter(status='draft').order_by('-date_of_publication')
        return context


class UpdateCourse(UpdateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'main/update_course.html'

    def get_success_url(self):
        return reverse_lazy('one_course', kwargs={'pk', self.object.pk})


class DeleteCourse(DetailView):
    model = Course
    template_name = 'main/course_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('one_course', kwargs={'pk', self.object.pk})


class UpdateLesson(UpdateView):
    model = Lesson
    form_class = CreateLessonForm
    template_name = 'main/update_lesson.html'

    def get_success_url(self):
        return reverse_lazy('one_lesson', kwargs={'pk', self.object.pk})


class DeleteLesson(DetailView):
    model = Lesson
    template_name = 'main/lesson_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('one_lesson', kwargs={'pk', self.object.pk})
