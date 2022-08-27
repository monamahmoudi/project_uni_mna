from dataclasses import fields
from pyexpat import model
from tkinter import Widget
from .models import Comment, postmodel
from django import forms

from A.models import postmodel


class searchform(forms.Form):
     search=forms.CharField()



class commentcreateform (forms.ModelForm):
     class Meta:
          model = postmodel
          fields = ('body', 'img')


class commentreplyform(forms.ModelForm):
     class  Meta:
          model = Comment
          fields = ('body',)
          Widgets ={
               'body':forms.Textarea(attrs={'class':'form-control'})  
          }



class postcreateupdateform(forms.ModelForm):
     class Meta:
          model = postmodel
          fields = ('title','body' , 'img')