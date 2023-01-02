from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from socialapp.models import Posts


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
                "first_name",
                "last_name",
                "username",
                "email",
                "password1",
                "password2",
                
                ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=[
        "title",
        "image"]
        widgets={
            "title":forms.Textarea(attrs={"class":"form-control","rows":3}),
            "image":forms.FileInput(attrs={"class":"form-select"})  
        }
        