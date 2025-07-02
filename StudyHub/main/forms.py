from django.forms import ModelForm, ClearableFileInput, TextInput, Select

from .models import Course


class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'level', 'cover']
        widgets = {
            'cover': ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_cover'
            }),
            'course_name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'level': Select(attrs={'class': 'form-select'})
        }