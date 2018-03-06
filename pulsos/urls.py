from django.urls import path

from .views import PulsoListView, PulsoCreateView

urlpatterns = [
    path(
        '<int:lat>/<int:long>/',
        PulsoListView.as_view(),
        name='pulso_list'
    ),
    path('', PulsoCreateView.as_view(), name='pulso_create')
]
