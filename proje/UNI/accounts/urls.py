from accounts import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name='accounts'
urlpatterns = [

     path("register/",views.RegisterView.as_view() , name='registerurl'),
     path('login/',views.loginview.as_view(),  name='loginurl'),
     path('reset/' ,views.resetpasswordview.as_view() , name='reset_password'),
     path('follow/user/<int:user_id>/' , views.followview.as_view() , name='followurl'),
     
     path('logout/',views.logoutview.as_view() ,name='logouturl'),
     path('profile/<int:user_id>/', views.profileview.as_view(), name='profileurl'),
     path('reset/done/' , views.passwordresetdoneview.as_view() , name='password_reset_done'),
     path('comfirm/<uidb64>/<token>/' , views.passwordresetconfirmview.as_view() , name='password_reset_confirm'),
     path('complete/' , views.passwordresetcomplateview.as_view() , name='password_reset_complete'),
     path('unfollow/user/<int:user_id>/' , views.unfollowview.as_view() , name='unfollowurl'),
     path('editprofile/' , views.edituserview.as_view() , name='editurl'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)