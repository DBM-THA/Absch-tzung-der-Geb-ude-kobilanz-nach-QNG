from django.urls import path
from . import views

urlpatterns = [
    path("", views.building_view, name="building"),
    path("scenario/", views.scenario_view, name="scenario"),
    path("projects/", views.project_list_view, name="projects"),
    path("project/<int:project_id>/", views.project_detail_view, name="project_detail"),
    path("project/<int:project_id>/compare/", views.compare_scenarios_view, name="compare_scenarios"),
]
