from django.urls import path

from .views import FollowerView, FollowingView

urlpatterns = [
    path('following/', FollowingView.as_view()),
    path('followers/', FollowerView.as_view())
]