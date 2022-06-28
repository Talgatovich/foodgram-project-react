from django.urls import include, path
from djoser import views

from .views import FollowViewSet

urlpatterns = [    
    path('users/subscriptions/', FollowViewSet.as_view(),
         name='subscription'),
    path('', include('djoser.urls')),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),

]
