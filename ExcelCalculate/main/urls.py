from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='main_index'),
    path('signup', views.signup, name='main_signup'),
    path('signup/join', views.join, name= 'main_join'),
    path('signin', views.signin, name='main_signin'),
    path('signin/login', views.login, name='main_login'),
    path('verifyCode', views.verifyCode, name='main_verifyCode'),
    path('verify', views.verify, name='main_verify'),
    path('result', views.result, name='main_result'),
    path('logout', views.logout, name = 'main_logout'),
    path('upload', views.upload, name = 'main_upload'),
    path('upload/posting', views.posting, name='main_posting'),
    
    path('blog', views.blog, name='main_blog'),
    path('upload/posting/<int:pk>/', views.new_post, name='main_new_post'),

    path('upload/posting/<int:pk>/upload/', views.remove_post, name= 'main_remove'),
]
