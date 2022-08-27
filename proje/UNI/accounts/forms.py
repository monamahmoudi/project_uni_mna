from .models import profile
from django import forms





class RegisterForm(forms.Form):
     username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
     email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))
     password1=forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
     password2=forms.CharField(label='password again',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class loginform (forms.Form):
     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))



class edituserform(forms.ModelForm):
     email = forms.EmailField(widget=forms.EmailInput(attrs={'calss':'form-control'}))
     class Meta:
          model = profile
          fields = ('age' , 'bio','image')