from django import forms
from django.forms import Select
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, levelChoices, departmentChoices
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomSelect(Select):
    def create_option(self, *args, **kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = True
            option['attrs']['selected'] = True

        """if option.get('value') == 2:
            option['attrs']['disabled'] = True"""

        return option


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}),
                             label="")

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field',
                                          'placeholder': 'Enter Password',
                                          'autocomplete': 'on'}),
        help_text="", label=""
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input-field',
                                          'placeholder': 'Confirm Password',
                                          'autocomplete': 'on'}),
        help_text=None, label=""
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}),
        }
        help_texts = {k: "" for k in fields}
        labels = {k: "" for k in fields}


class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}),
                             label="")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input-field', 'placeholder': 'Confirm Password', 'autocomplete': 'on'}),
        label="")


class UpdateProfileForm(forms.ModelForm):
    level = forms.ChoiceField(widget=CustomSelect(attrs={'class': 'select-field'}),
                              choices=levelChoices, label="")

    department = forms.ChoiceField(widget=CustomSelect(attrs={'class': 'select-field'}),
                                   choices=departmentChoices, label="")

    class Meta:
        model = Profile
        fields = ['level', 'department', 'image']
        help_texts = {k: "" for k in fields}
        labels = {k: "" for k in fields}


