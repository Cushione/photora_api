from django.urls import path
from posts import views

urlpatterns = [
    path('posts', views.PostList.as_view()),
    path('posts/feed', views.FollowPostList.as_view()),
    path('posts/<int:id>', views.PostDetail.as_view()),
    path('posts/<int:id>/likes', views.PostLike.as_view()),
    path('posts/search', views.PostSearch.as_view()),
    path('profiles/<int:id>/posts', views.ProfilePosts.as_view())
]