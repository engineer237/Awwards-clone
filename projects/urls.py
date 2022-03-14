from  django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-post/', views.create_post, name='create-post'),
    path('like-post/', views.like_post, name='like')
]

