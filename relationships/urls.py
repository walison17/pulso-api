from django.urls import path

from .views import FollowerListView

urlpatterns = [
    path('<int:pk>/followers/', FollowerListView.as_view()),
    # path('following/<int:pk>/', UnfollowView.as_view()),
]
