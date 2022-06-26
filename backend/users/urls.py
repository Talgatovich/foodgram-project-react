from django.urls import include, path
from djoser import views
from rest_framework.routers import SimpleRouter

from .views import FollowViewSet

router = SimpleRouter()

router.register('users/subscriptions/', FollowViewSet, basename="subscriptions")

urlpatterns = [
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    
    
]
