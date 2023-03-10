from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/user', views.UserProfile.as_view()),
    path('profiles/<int:id>', views.ProfileDetail.as_view()),
    path('profiles/<int:id>/followers', views.ProfileFollow.as_view()),
]