from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from fcm_django.api.rest_framework import FCMDeviceViewSet

from accounts import views
from relationships import views as rel_views
from notifications.views import FirebaseDeviceViewSet


router = SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'me/devices', FirebaseDeviceViewSet, 'device')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/<str:backend>', views.get_token),
    path('me/', include([
        path('', views.me),
        path('following/', rel_views.FollowingView.as_view()),
        path('followers/', rel_views.FollowerView.as_view()),
        path('following/<int:pk>/', rel_views.UnfollowView.as_view()),
        path('facebook_friends/', views.FacebookFriendListView.as_view()),
    ])),
    path('', include(router.urls)),
]
