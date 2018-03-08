from django.urls import path, re_path

from .views import PulsoListView, PulsoCreateView

urlpatterns = [
    path('', PulsoCreateView.as_view(), name='pulso_create'),
    re_path(
        r'^(?P<lat>-?\d{1,3}.\d+)/(?P<long>-?\d{1,3}.\d+)/$',
        PulsoListView.as_view(),
        name='pulso_list'
    ),
]
