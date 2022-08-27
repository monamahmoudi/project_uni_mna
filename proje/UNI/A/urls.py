from django import views
from A import views
from django.urls import path

app_name='A'
urlpatterns = [

     path('',views.homeview.as_view() , name='homeurl'),
     path('post/<int:post_id>/<slug:post_slug>/' , views.postdetailview.as_view() ,name='posturl'),
     path('create/' , views.createpostview.as_view() , name='createurl'),
     path('like/<int:post_id>/', views.postlikeview.as_view(), name='likeurl'),
     path('dislike/<int:post_id>/', views.postdislikeview.as_view(), name='dislikeurl'),
     path('delete/<int:post_id>/', views.deletepostview.as_view(), name='deleteurl'),
     path('update/<int:post_id>/', views.postupdateformview.as_view(), name='updateurl'),
     path('reply/<int:post_id>/<int:comment_id>/' , views.postaddreplyview.as_view() ,name='reply'),


]