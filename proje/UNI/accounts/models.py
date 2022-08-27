from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


class Relation (models.Model):
     from_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='followers')
     to_user = models.ForeignKey(User , on_delete= models.CASCADE , related_name='following')
     created = models.DateTimeField(auto_now_add=True)
     
     def __str__(self):
          return f'{self.from_user}following {self.to_user}'
           

class profile(models.Model):
    user=models.OneToOneField(User , on_delete=models.CASCADE ,related_name='profile' )
    age=models.PositiveSmallIntegerField(default=0)
    bio=models.TextField(null=True , blank=True)
    image = models.ImageField(null=True,upload_to = 'image_profile/')
    
    def __str__(self) :
         return f'{self.user}  ... {self.age}' 
    

    