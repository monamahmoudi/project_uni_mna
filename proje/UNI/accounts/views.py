from re import I
from django.contrib import messages
from pyexpat.errors import messages
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login ,authenticate ,logout
from django.http import HttpResponse
from  .forms import *
from django.contrib.auth import views as auth_views
from django.urls import  reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation,profile
from accounts.models import Relation
from A.models import postmodel


class RegisterView(View):
     def dispatch(self, request, *args, **kwargs):
          if request.user.is_authenticated:
               return redirect('A:homeurl')
          return super().dispatch(request, *args, **kwargs)

     def get(self,request):
          form=RegisterForm()
          return render(request, 'accounts/register.html',{'form':form})

     def post (self , request):
          
          cd = request.POST
          if User.objects.filter(email=cd['email']).exists():
               messages.info(request,'email warniing','info')
               
               return redirect ('accounts:registerurl')



          if cd ['password'] == cd ['password2']:
               try:
                    user = User.objects.create_user(email = cd['email'] , username = cd['username'] , password = cd['password'])
                    profile.objects.create(user = user)
                    messages.success(request,'user registered','success')
                    return redirect ('accounts:loginurl')
               except:
                    messages.info(request , 'Error' , 'info')
                    return redirect ('accounts:registerurl')

          else:
               messages.info(request , 'username password not math' , 'info')
               return redirect ('accounts:registerurl')


class loginview (View):
     def dispatch(self , request , *args , **kwargs):
          if request.user.is_authenticated:
               return redirect('A:homeurl')
          return super().dispatch(request, *args , **kwargs)

     def get (self , request):
          form = loginform
          return render(request , 'accounts/login.html' , {'form':form}) 

     def post(self , request ):
          username = request.POST ['username']
          password = request.POST ['password']
          user = authenticate(request , username=username, password=password)
          if user is not None:
               login(request , user)
               return redirect('A:homeurl')
          messages.info(request, 'username or password invalid' , 'info')
          return redirect('accounts:logouturl')
          




class resetpasswordview(auth_views.PasswordResetView):
     template_name: 'accounts/password_reset_form.html'
     success_url=reverse_lazy('accounts:password_reset_done')
     email_template_name='accounts/password_reset_email.html'


class logoutview (LoginRequiredMixin , View):

     def get (self , request):
          logout(request)
          messages.success(request , 'logout successful' , 'success')
          return redirect ('accounts:loginurl')


class profileview(LoginRequiredMixin , View):
     def get (self , request , user_id ):
          is_following = False
          user = User.objects.get(pk= user_id)
          posts = postmodel.objects.filter(user=user)
          relation =Relation.objects.filter(from_user= request.user , to_user= user)
          if relation.exists():
               is_following = True
          return render (request , 'accounts/profile.html' , {'user':user , 'posts':posts , 'is_following':is_following})



class resetpasswordview(auth_views.PasswordResetView):
     template_name='accounts/password_reset_form.html'
     success_url=reverse_lazy('accounts:password_reset_done')
     email_template_name='accounts/password_reset_email.html'


class passwordresetdoneview(auth_views.PasswordResetDoneView):
     template_name='accounts/password_reset_done.html'


class passwordresetconfirmview(auth_views.PasswordResetConfirmView):
     template_name='accounts/password_reset_confirm.html'
     success_url=reverse_lazy('accounts:password_reset_complete')


class passwordresetcomplateview(auth_views.PasswordResetCompleteView):
     template_name='accounts/password_reset_complete.html'


class followview( LoginRequiredMixin , View):
     def get (self , request , user_id  ):
          
          # post = postmodel.objects.get(id = post_id)
          user = User.objects.get(id = user_id)
          relation = Relation.objects.filter(from_user = request.user , to_user = user)
          if relation.exists():
               messages.error(request , 'you are already following this user;', 'danger')
          else:
               Relation.objects.create(from_user = request.user , to_user = user)
               messages.success(request , 'you following this user' , 'info')
          return redirect ('accounts:profileurl' ,user_id) 
          



class unfollowview (LoginRequiredMixin , View):
     def get (self , request , user_id ):
          # post = postmodel.objects.get(id = post_id)

          user = User.objects.get(id = user_id)
          relation = Relation.objects.filter(from_user = request.user , to_user = user)
          if relation.exists():
               relation.delete()
               messages.success(request , 'you unfollowing this user' , 'info' )
          else:
               messages.error(request , 'you are not following this user' , 'danger')
          return redirect ('accounts:profileurl' ,user_id) 


class edituserview(LoginRequiredMixin , View):
     form_class = edituserform

     def get(self , request):
          form = self.form_class(instance = request.user.profile , initial ={'email':request.user.email})
          return render(request , 'accounts/editprofile.html' , {'form':form})
          

     def post (self , request):
          form = self.form_class(request.POST,request.FILES , instance=request.user.profile)
          
          if form.is_valid:
               
               form.save()
               request.user.email = form.cleaned_data['email']
               request.user.save()
               messages.success(request , 'edit successful' , 'success')
          return redirect ('accounts:profileurl' , request.user.id)



