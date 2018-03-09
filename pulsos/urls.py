from django.urls import path, re_path

from .views import (PulsoListView, PulsoCreateView,
                    PulsoCloseView, PulsoDetailCancelView)

urlpatterns = [
    path('', PulsoCreateView.as_view(), name='pulso_create'),
    re_path(
        r'^(?P<lat>-?\d{1,3}.\d+)/(?P<long>-?\d{1,3}.\d+)/$',
        PulsoListView.as_view(),
        name='pulso_list'
    ),
    path('<int:pk>/', PulsoDetailCancelView.as_view()),
    path('<int:pk>/close/', PulsoCloseView.as_view(), name='pulso_close')
]
