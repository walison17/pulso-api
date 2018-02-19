from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from accounts import views
from relationships import views as rel_views


router = SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/<str:backend>', views.get_token),
    path('me/', views.me),
    path('me/following/', rel_views.FollowingView.as_view()),
    path('me/followers/', rel_views.FollowerView.as_view()),
    path('', include(router.urls)),
]
