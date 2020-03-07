from django import forms
from django.contrib.auth.models import User
from macro_mate.models import User_Profile 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class User_ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User_Profile
        fields = ('profilePicture',)

