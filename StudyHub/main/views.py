from decimal import Decimal

from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import models
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, DeleteView
from .mixins import NotesMixin

from .forms import CreateCourseForm, LoginForm, SignupForm, CreateLessonForm, FeedbackForm
from .models import Course, UserProfile, Lesson, Review, Note, CourseLesson, Progress, LessonViewLog


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_obj = self.request.user
        context['favorites'] = user_obj.favorites.all()
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_lesson = CourseLesson.objects.filter(course=self.get_object()).order_by('order')
        context['ordered_lesson'] = [cl.lesson for cl in class_lesson]
        return context



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


class OneLesson(DetailView, NotesMixin):
    model = Lesson
    template_name = 'main/one_lesson.html'
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context['notes'] = self.get_notes(lesson)
        return context



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


def change_status(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.status == 'draft':
        course.status = 'published'
    else:
        course.status = 'draft'
    course.save()
    return redirect('profile', pk=request.user.pk)


class ChangePassword(FormView):
    form_class = PasswordChangeForm
    template_name = 'main/change_password.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk' : self.request.user.pk})

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return super().form_valid(form)

class Search(ListView):
    model = Course
    template_name = 'main/search.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Course.objects.filter(course_name__icontains=query, status='published')
        return Course.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class Favorites(ListView):
    model = Course
    template_name = 'main/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        user_obj = get_object_or_404(UserProfile, pk=self.request.user.pk)
        return user_obj.favorites.all()


def fav_status_change(request, pk):
    course = get_object_or_404(Course, pk=pk)
    user_obj = request.user

    if course in user_obj.favorites.all():
        user_obj.favorites.remove(course)
    else:
        user_obj.favorites.add(course)

    return redirect('main_page')

class Feedback(FormView):
    model = Review
    form_class = FeedbackForm
    template_name = 'main/feedback.html'
    success_url = 'main_page'

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'skip':
            return redirect('main_page')

        rate = form.cleaned_data.get('rate')
        if not rate:
            form.add_error('rate', 'Please rate or skip')
            return self.form_invalid(form)

        Review.objects.create(
            user = self.request.user,
            course = Course.objects.get(pk=self.kwargs['pk']),
            rate = rate,
            comment = form.cleaned_data.get('comment', '')
        )
        return redirect('main_page')


def create_note(request, pk):
    def get_availability():
        if request.POST.get('is_private') == 'on':
            return 'private'
        return 'public'

    Note.objects.create(
        lesson = Lesson.objects.get(pk=pk),
        user = request.user,
        content = request.POST.get('note'),
        availability = get_availability()
    )

    return redirect('one_lesson', pk)


def update_note(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.user != note.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            note.content = content
            note.save()

    return redirect('one_lesson', pk=note.lesson.pk)


class DeleteNote(DeleteView):
    model = Note

    def get_success_url(self):
        return reverse_lazy('one_lesson', kwargs={'pk': self.object.lesson.pk})


def add_to_course(request, pk):
    course_id = request.POST.get('course_id')
    course = get_object_or_404(Course, pk=course_id)
    lesson = get_object_or_404(Lesson, pk=pk)

    last_order = (CourseLesson.objects.filter(course=course).aggregate(max_order=models.Max('order'))['max_order']) or 0

    CourseLesson.objects.create(course=course, lesson=lesson, order=last_order + 1)

    return redirect('profile', pk=request.user.pk)


class StartCourse(View, NotesMixin):
    template_name = 'main/lesson_course.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course_lesson = get_object_or_404(CourseLesson, course=course, order=1)
        lesson = course_lesson.lesson
        notes = self.get_notes(lesson)

        return render(request, self.template_name, {
            'lesson': lesson,
            'notes': notes,
            'course_pk': pk,
            'order': 1
        })

class FlipPage(View, NotesMixin):
    template_name = 'main/lesson_course.html'

    def get(self, request, pk):
        direction = request.GET.get('flip')
        order = request.GET.get('order')
        course = get_object_or_404(Course, pk=pk)
        last = CourseLesson.objects.filter(course=course).count()
        if direction == 'next':
            next_order = int(order) + 1
            course_lesson = get_object_or_404(CourseLesson, course=course, order=next_order)
        else:
            next_order = int(order) - 1
            course_lesson = get_object_or_404(CourseLesson, course=course, order=next_order)
        lesson = course_lesson.lesson
        complete_button  = LessonViewLog.objects.filter(
            user=request.user,
            course=course,
            lesson=lesson
        ).exists()
        notes = self.get_notes(lesson)

        LessonViewLog.objects.create(
            user=self.request.user,
            course=course,
            lesson=lesson
        )

        return render(request, self.template_name, {
            'lesson': lesson,
            'notes': notes,
            'course_pk': pk,
            'order': next_order,
            'first': next_order == 1,
            'last': next_order == last,
            'completed': complete_button
        })


class LessonDone(View):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs['course_pk'])
        total = CourseLesson.objects.filter(course=course).count()
        compile_num = Progress.objects.filter(user=request.user, course=course).count() + 1
        precent_of_complete = round(Decimal(compile_num) / Decimal(total) * 100, 2)
        # Отлавливать IntegrityError на нарушение unique_together
        Progress.objects.create(
            user = request.user,
            course = course,
            precent_of_complete = precent_of_complete
        )
        print(request.POST.get('path'))
        return redirect(request.POST.get('path'))

