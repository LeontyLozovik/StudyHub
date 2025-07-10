from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, ClearableFileInput, TextInput, Select, Textarea

from .models import Course, UserProfile, Lesson


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )

class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Same password'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Tell us something about yourself',
        'rows': 4,
    }))
    country = forms.ChoiceField(
        required=False,
        choices=UserProfile._meta.get_field('country').choices,
        initial='BY',
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_avatar'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'bio', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['bio'].label = 'Biography'

class CreateCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'description', 'level', 'cover']
        widgets = {
            'cover': ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_cover',
            }),
            'course_name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'level': Select(attrs={'class': 'form-select'})
        }

class CreateLessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_name', 'description', 'video']
        widgets = {
            'lesson_name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'video': ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_video',
                'style': 'display: none;',
                'accept': 'video/*'
            }),
        }