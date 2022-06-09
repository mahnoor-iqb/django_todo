from django.urls import path
from user.views import (
    UserApiView,
    UserDetailApiView
)

urlpatterns = [
    path('users', UserApiView.as_view()),
    path('users/<int:user_id>', UserDetailApiView.as_view()),
]
