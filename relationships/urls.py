from django.urls import path

from .views import FollowerView, FollowingView, UnfollowView

urlpatterns = [
    path('following/', FollowingView.as_view()),
    # path('following/<int:pk>/', UnfollowView.as_view()),
    path('followers/', FollowerView.as_view())
]