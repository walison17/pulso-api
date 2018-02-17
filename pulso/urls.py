from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from accounts import views

router = SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/<str:backend>', views.get_token),
    path('me/', views.me),
    path('me/', include('relationships.urls')),
    path('', include(router.urls)),
]
