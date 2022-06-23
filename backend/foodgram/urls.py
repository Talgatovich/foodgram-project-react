from django.contrib import admin
from django.urls import include, path

api_paths = [
    path('', include('users.urls')),
    #path('', include('recipes.urls'))
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_paths))
]
