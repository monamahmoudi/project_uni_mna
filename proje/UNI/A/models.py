from turtle import title
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class postmodel(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE )
     title = models.CharField(max_length=50,null=True)
     price = models.IntegerField(default=0)
     body = models.TextField(max_length=100)
     slug = models.SlugField()
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     img =models.ImageField(upload_to='folderimages/',null=True)

     class Meta:
        ordering = ('-created',)

     def __str__(self):
        return self.slug

     def get_absolute_url(self):
        return reverse('A:posturl' , args=(self.pk , self.slug))

     def like_count(self):
        return self.plike.count()

     def user_can_like(self , user):
        user_like=user.ulike.filter(post=self)
        if user_like.exists():
            return True
        return False
                     

class Comment (models.Model):
   user = models.ForeignKey(User , on_delete=models.CASCADE , related_name=  'ucomments')
   post = models.ForeignKey(postmodel , on_delete=models.CASCADE , related_name='pcomments')
   # reply= models.ForeignKey('self' , on_delete=models.CASCADE , related_name='rcomments' , blank=True , null=True)
   # is_reply = models.BooleanField(default=False)
   body = models.TextField(max_length=400)
   created = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return f'{self.user} - {self.body [:30]}'



class Like(models.Model):
      user=models.ForeignKey(User , on_delete=models.CASCADE, related_name='ulike')
      post=models.ForeignKey(postmodel , on_delete=models.CASCADE , related_name='plike')

      def __str__(self):
        return f'{self.user}liked{self.post.slug}'