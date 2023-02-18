from django.urls import path
from posts import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:id>', views.PostDetail.as_view()),
    path('posts/<int:id>/likes', views.PostLike.as_view()),
]