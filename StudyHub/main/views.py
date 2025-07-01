from django.shortcuts import render
from django.views.generic import CreateView

from .models import Course


# Create your views here.

class CreateCourse(CreateView):
    model = Course
    form = CreateCourseForm