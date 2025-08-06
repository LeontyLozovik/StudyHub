from django import template

from main.models import Progress

register = template.Library()


@register.simple_tag
def course_progress(user, course_pk):
    progress = Progress.objects.filter(user=user, course__pk=course_pk).values_list('precent_of_complete', flat=True).last() or 0
    return progress