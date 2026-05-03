from django.urls import path
from . import views

urlpatterns = [
    path("", views.building_view, name="building"),
    path("scenario/", views.scenario_view, name="scenario"),
]
