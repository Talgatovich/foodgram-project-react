from django.urls import include, path
from djoser import views

from .views import FollowCreateAPIView, FollowListAPIView

urlpatterns = [
    path(
        "users/<int:id>/subscribe/",
        FollowCreateAPIView.as_view(),
        name="subscribe",
    ),
    path(
        "users/subscriptions/",
        FollowListAPIView.as_view(),
        name="subscriptions",
    ),
    path("auth/token/login/", views.TokenCreateView.as_view(), name="login"),
    path(
        "auth/token/logout/", views.TokenDestroyView.as_view(), name="logout"
    ),
    path("", include("djoser.urls")),
]
