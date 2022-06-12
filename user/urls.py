from django.urls import path
from user.views import (
    UserApiView,
    UserDetailApiView
)

urlpatterns = [
    path('', UserApiView.as_view(), name="user_api"),
    path('<int:user_id>', UserDetailApiView.as_view(), name="user_detail_api"),
]
