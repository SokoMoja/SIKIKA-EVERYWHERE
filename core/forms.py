from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, LectureSession, SessionSlide


class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('lecturer', 'Lecturer'),
        ('student', 'Student'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']


class LectureSessionForm(forms.ModelForm):
    class Meta:
        model = LectureSession
        fields = ['title', 'course_code']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Database Systems - Lecture 7'}),
            'course_code': forms.TextInput(attrs={'placeholder': 'e.g. CS301'}),
        }


class JoinSessionForm(forms.Form):
    session_code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code', 'style': 'text-transform: uppercase;'}),
    )
    mode = forms.ChoiceField(choices=[
        ('caption', 'Smart Captions (Deaf / Hard-of-hearing)'),
        ('audio', 'Audio Description (Blind / Low-vision)'),
        ('sign', 'Sign Language'),
    ])


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class SlideUploadForm(forms.Form):
    slides = forms.FileField(
        widget=MultipleFileInput(attrs={'accept': 'image/*'}),
        help_text='Upload slide images (PNG, JPG). Select multiple files.',
    )


class AccessibilityForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['font_size', 'high_contrast', 'dyslexia_font', 'preferred_mode']
        widgets = {
            'font_size': forms.Select(attrs={'class': 'form-select'}),
            'preferred_mode': forms.Select(attrs={'class': 'form-select'}),
        }
