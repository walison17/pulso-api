from django.urls import path

from .views import CommentListCreateView

urlpatterns = [
    path('<int:pk>/comments/', CommentListCreateView.as_view(), name='comment_create')
]
