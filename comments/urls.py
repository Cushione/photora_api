from django.urls import path
from comments import views

urlpatterns = [
    path('posts/<int:post_id>/comments', views.CommentList.as_view()),
    path('posts/<int:post_id>/comments/<int:id>', views.CommentDetail().as_view()),
]