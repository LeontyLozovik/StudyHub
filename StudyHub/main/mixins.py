from django.db.models import Max, Avg
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import CourseLesson, Course, Review


class NotesMixin:
    def get_notes(self, lesson):
        filter_type = self.request.GET.get('filter', 'all')

        if filter_type == 'my':
            return lesson.notes_to_lesson.filter(user=self.request.user)
        elif filter_type == 'private':
            return lesson.notes_to_lesson.filter(user=self.request.user, availability='private')
        else:
            return lesson.notes_to_lesson.filter(availability='public')

class ReviewMixin:
    def get_review(self, course):
        return Review.objects.filter(course=course)

    def get_average_rate(self, course):
        avg = Review.objects.filter(course=course).aggregate(avg_rate=Avg('rate'))['avg_rate']
        return round(float(avg), 1) if avg is not None else 0.0

class FlipLessonMixin:
    def flip(self, course, direction, order):
        if direction == 'next':
            next_order = int(order) + 1
            course_lesson = CourseLesson.objects.filter(course=course, order=next_order).first()
            if not course_lesson:
                max_order = CourseLesson.objects.filter(course=course).aggregate(Max('order'))['order__max']
                next_order = max_order
                course_lesson = CourseLesson.objects.filter(course=course, order=max_order).first()
        elif direction == 'prev':
            next_order = int(order) - 1
            course_lesson = CourseLesson.objects.filter(course=course, order=next_order).first()
            if not course_lesson:
                next_order = 1
                course_lesson = CourseLesson.objects.filter(course=course, order=1).first()
        else:
            return Http404
        return course_lesson, next_order

class FinishMixin:
    def finish(self, course_pk):
        user = self.request.user
        course = get_object_or_404(Course, pk=course_pk)
        user.started.remove(course)
        user.finished.add(course)