from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreateCourseForm
from .models import Course


# Create your views here.

class CreateCourse(CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'main/course_form.html'

class MainPage(ListView):
    model = Course
    template_name = 'main/main_page.html'
    context_object_name = 'courses'
    paginate_by = 8
    ordering = ['-date_of_publication']