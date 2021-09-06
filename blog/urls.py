from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('<slug:slug>/', views.blogDetail, name='blog_detail'),
    path('<slug:slug>/addContent/', views.addContent, name='add_content'),
    path('<slug:slug>/like/', views.like, name='blog_likes'),
    path('<slug:slug>/dislike/', views.dislike, name='blog_dislike'),
    path('<slug:slug>/update/', views.UpdateBlogView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', views.DeleteBlogView.as_view(), name='blog_delete'),
    path('create/new/', views.CreateBlogView.as_view(), name='new_post'),






]



