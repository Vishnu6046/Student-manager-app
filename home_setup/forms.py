from django import forms
from .models import StudentProfile, Subject, Mark, Department
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.password_validation import validate_password

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['department']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject', 'marks_obtained']

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)

        if student:
            self.fields['subject'].queryset = Subject.objects.filter(department=student.department)

def only_letters(value):
    if not re.match(r'^[A-Za-z\s]+$', value):
        raise ValidationError("Only alphabets are allowed.")

class StudentCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150, required=True, validators=[only_letters])
    last_name = forms.CharField(max_length=150, required=True, validators=[only_letters])
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = StudentProfile
        fields = ['department']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        if not re.search(r'[A-Za-z]', username):
            raise forms.ValidationError("Username must contain at least one letter.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores (_).")

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        
        validate_password(password)

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", password):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        student = StudentProfile(
            user=user,
            department=self.cleaned_data['department']
        )
        if commit:
            student.save()
        return student

class EditStudentUserForm(forms.ModelForm):
    first_name = forms.CharField(required=True,
    validators=[only_letters],
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
    required=True,
    validators=[only_letters],
    widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
    required=True,
    widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']