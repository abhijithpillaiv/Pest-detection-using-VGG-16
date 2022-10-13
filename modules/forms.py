from django.db import models
from django import forms
from modules.models import user_reg,farmer_reg,krishireg,feed,solreq


class ListForm(forms.ModelForm):
    class Meta:
        model=user_reg
        fields=("name", "email", "password1", "password2")

class ListForm1(forms.ModelForm):
    class Meta:
        model=farmer_reg
        fields=("name","address","phone","email","place","pincode", "password1", "password2")

class ListForm3(forms.ModelForm):
    class Meta:
        model=krishireg
        fields=("name","address","phone","email","city","pincode", "password1", "password2")        

class ListForm2(forms.ModelForm):
    class Meta:
        model=user_reg
        fields=( "email", "password1")        

class ListForm4(forms.ModelForm):
    class Meta:
        model=feed
        fields=( "name","email", "description") 

class ListForm5(forms.ModelForm):
    class Meta:
        model=solreq
        fields=( "name","email", "description")          


# Create your models here.
