from django.urls import path
from .views import LoginJWTView, RefreshJWTView, UsersAPIView, LogOutAPIView



urlpatterns =[
    path("login/", LoginJWTView.as_view(), name="login-view"),
    path("refresh/", RefreshJWTView.as_view(), name="refresh-token"),
    path("all-users/", UsersAPIView.as_view(), name="all-users"),
    path("logout/", LogOutAPIView.as_view(), name="logout")
]