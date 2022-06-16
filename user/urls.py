from django.urls import path
from user.views import (
    AdminView,
    AdminDetailView,
    UserDetailView,
    SignupView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('', AdminView.as_view(), name="admin_api"),
    path('delete/<int:user_id>', AdminDetailView.as_view(), name="admin_delete_api"),
    path('<int:user_id>', UserDetailView.as_view(), name="user_detail_api"),
    path('signup', SignupView.as_view(), name="signup"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
