# urls.py
from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('post_list/', views.post_list, name='post_list'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]
