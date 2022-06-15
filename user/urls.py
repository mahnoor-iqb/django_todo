from django.urls import path
from user.views import (
    UserApiView,
    UserDetailApiView,
    SignupView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('', UserApiView.as_view(), name="user_api"),
    path('<int:user_id>', UserDetailApiView.as_view(), name="user_detail_api"),
    path('signup', SignupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
