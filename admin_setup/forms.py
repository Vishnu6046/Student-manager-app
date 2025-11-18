from django import forms
from django.contrib.auth.models import User
from home_setup.models import Department, StudentProfile, StaffProfile, Position
from profile_setup.models import Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re
from django.contrib.auth.password_validation import validate_password
from .models import AdminProfile


class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        if not re.search(r'[A-Za-z]', username):
            raise forms.ValidationError("Username must contain at least one letter.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores (_).")

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")

        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match.")
        if len(pass2) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r"[A-Z]", pass2):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", pass2):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", pass2):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", pass2):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
            
        return pass2

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ['department', 'position']


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title']

class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'password1', 'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")

        if not re.search(r'[A-Za-z]', username):
            raise forms.ValidationError("Username must contain at least one letter.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores (_).")

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only letters.")
        return last_name

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")

        if pass1 != pass2:
            raise forms.ValidationError("Passwords do not match.")
        if len(pass2) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r"[A-Z]", pass2):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", pass2):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", pass2):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[@$!%*?&]", pass2):
            raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
            
        return pass2

