from django import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from A.forms import searchform , commentcreateform , commentreplyform , postcreateupdateform
from accounts.models import Relation
from .models import postmodel , Like ,Comment
from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils. text import slugify


class homeview ( LoginRequiredMixin,View):
     form_class = searchform
     
     def get(self,request ):
         
          posts = postmodel.objects.all()
          if request.GET.get('search'):
               posts = posts.filter(slug__contains=request.GET['search'])
          return render(request,'home/home.html', {'posts': posts , 'form':self.form_class})
        
     
     


class postdetailview (View):
     form_class = commentcreateform
     form_class_reply = commentreplyform
     

     def setup(self, request ,*args, **kwargs):
          self.post_instance = get_object_or_404(postmodel , pk = kwargs['post_id'] , slug = kwargs['post_slug'])
          return super().setup(request , *args , **kwargs)

     
     def get (self , request , post_id , post_slug):
          posts = postmodel.objects.get(pk = post_id , slug = post_slug)
          
          comments = posts.pcomments.all()
          like = Like.objects.filter(user=request.user,post=posts).exists()
          relation = Relation.objects.filter(from_user=request.user , to_user =self.post_instance.user ).exists()
          like_count = Like.objects.filter(post = posts).count()
          
          can_like = True
          can_fallow =True
          if request.user.is_authenticated and relation:
               can_fallow = False
          if request.user.is_authenticated and like:
               can_like = False
          return render(request , 'home/details.html' , {'posts':posts , 'comments':comments   , 'canlike':can_like,'canfallow':can_fallow,'like_count':like_count})


     def post(self , request , *args , **kwargs):
          comment =request.POST['comment']
          Comment.objects.create(user = request.user,post =self.post_instance,body=comment )
          messages.success(request , 'your comment submit successful' , 'success')

          return redirect('A:posturl' , self.post_instance.id , self.post_instance.slug)

          # form = self.form_class(request.POST)
          # if form.is_valid:
          #      new_comment = form.save(commit = False)
          #      new_comment.user = request.user
          #      new_comment.post = self.post_instance
          #      new_comment.save()
          #      messages.success(request , 'your comment submit successful' , 'success')
          #      return redirect('home:posturl' , self.post_instance.id , self.post_instance.slug)

     
class createpostview (LoginRequiredMixin , View):
     form_class= postcreateupdateform

     def get(self , request , *args , **kwargs):
          form = self.form_class
          return render(request ,'home/create.html' , {'form':form})

     def post (self , request , *args , **kwargs):
          cd = request.POST
          
          img = request.FILES
          post = postmodel.objects.create(user= request.user,title = cd['title'],
          body = cd['caption'],img=img['img']
          )
          post.slug=slugify(cd['caption'])[:30]
          post.save()
          messages.success(request,'created post successfull' , 'success')
          return redirect('A:posturl', post.id ,post.slug)

          
          # form = self.form_class(request.POST,request.FILES['img'])
          # if form.is_valid():
               
          #      new_post = form.save(commit=False)
          #      new_post.slug= slugify(form.cleaned_data['body'][:30])
          #      new_post.user=request.user
          #      new_post.save()
               
          #      messages.success(request,'created post successfull' , 'success')
          #      return redirect('A:posturl', new_post.id ,new_post.slug)


class postlikeview(LoginRequiredMixin , View):
     def get (self, request, post_id):
          post=get_object_or_404(postmodel ,id=post_id)
          like=Like.objects.filter(post=post , user=request.user)
          if like.exists():
               messages.error(request, 'You liked it before' ,'danger')
          else:
               Like.objects.create(post=post, user=request.user)
               messages.success(request , 'liked successfully' , 'success')
          return redirect('A:posturl' , post.id , post.slug)

class postdislikeview(LoginRequiredMixin,View):
     def get (self, request, post_id):
          post=get_object_or_404(postmodel ,id=post_id)
          like=Like.objects.filter(post=post , user=request.user)
          if like.exists():
               like.delete()
               messages.error(request, 'You disliked' ,'danger')
          else:
              
               messages.success(request , 'you not like this post' , 'success')
          return redirect('A:posturl' , post.id , post.slug)


class deletepostview(LoginRequiredMixin , View):
     def get(self , request , post_id):
          post= postmodel.objects.get(pk=post_id)
          if post.user.id == request.user.id:
               post.delete()
               messages.success(request, 'deleted post successfull' , 'success')

          else:
               messages.error(request , 'You can not delete the post')
          return redirect('A:homeurl')


class postupdateformview(LoginRequiredMixin, View):
     form_class=postcreateupdateform
     def setup(self, request, *args, **kwargs):
          self.post_instance=postmodel.objects.get(pk=kwargs['post_id'])
          return super().setup(request, *args, **kwargs)
     
     def dispatch(self, request, *args, **kwargs):
          post = self.post_instance
          if not post.user.id == request.user.id:
               messages.error(request, 'Update failed' ,'danger')
               return redirect('A:homeurl')
          return super().dispatch(request, *args, **kwargs)


     def get(self , request, *args , **kwargs):
          post= self.post_instance
          form= self.form_class(instance=post)
          
          return render(request , 'home/update.html' , {'form':form})
    
    
     def post(self , request, *args ,**kwargs):
          post=self.post_instance
          form=self.form_class(request.POST,request.FILES , instance=post)
          if form.is_valid:
               new_post=form.save(commit=False)
               new_post.slug=slugify(form.cleaned_data['body'][:30])
               new_post.save()
               messages.success(request,'updated successfull' , 'success')
               return redirect('A:posturl' , post.id , post.slug)
         
class postaddreplyview(LoginRequiredMixin, View):
     form_class= commentreplyform

     def post(self , request , post_id , comment_id):
          post=get_object_or_404(postmodel,id=post_id)
          comment=get_object_or_404(Comment , id=comment_id)
          form=self.form_class(request.POST)
          if form.is_valid():
               reply=form.save(commit=False)
               reply.user=request.user
               reply.post=post
               reply.reply=comment
               reply.is_reply=True
               reply.save()
               messages.success(request, 'reply is successfully' , 'success')
          return redirect('A:posturl' , post.id , post.slug)

