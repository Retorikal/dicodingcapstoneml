from .models import Order
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class orderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class createUserForm(UserCreationForm):
    fullname = forms.CharField(label = "Fullname")
    linkedin =forms.CharField(label="linkedin")
    age=forms.IntegerField(label="age")
    user_cv =forms.FileField(label="user_cv")
    class Meta:
        model = User
        fields=["username","email","password1","password2","fullname","linkedin","age","user_cv"]
    
    def save(self, commit=True):
        user = super(createUserForm, self).save(commit=False)
        fullname= self.cleaned_data["fullname"]
        linkedin = self.cleaned_data["linkedin"]
        age=self.cleaned_data["age"]
        user_cv = self.cleaned_data["user_cv"]
        user.linkedin = linkedin
        user.fullname = fullname
        user.age=age
        user.cv=user_cv
        if commit:
            user.save()
        return user


