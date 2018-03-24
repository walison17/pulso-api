from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from rest_framework.routers import SimpleRouter

from accounts import views
from relationships import views as rel_views
from push_notifications.views import FirebaseDeviceViewSet, NotificationViewSet


router = SimpleRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'me/devices', FirebaseDeviceViewSet, 'devices')
router.register(r'me/notifications', NotificationViewSet, 'notifications')

urlpatterns = [
    path('termos-de-uso/', TemplateView.as_view(template_name='termos-de-uso.html')),
    path(
        'politica-de-privacidade',
        TemplateView.as_view(template_name='politica-de-privacidade.html'),
    ),
    path('pulsos/', include('pulsos.urls')),
    path('pulsos/', include('comments.urls')),
    path('admin/', admin.site.urls),
    path('auth/<str:backend>', views.get_token),
    path(
        'me/',
        include(
            [
                path('', views.me),
                path('following/', rel_views.FollowingView.as_view()),
                path('followers/', rel_views.FollowerView.as_view()),
                path('following/<int:pk>/', rel_views.UnfollowView.as_view()),
                path('facebook_friends/', views.FacebookFriendListView.as_view()),
            ]
        ),
    ),
    path('', include(router.urls)),
]
