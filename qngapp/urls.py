from django.urls import path
from . import views

urlpatterns = [
    path("", views.building_view, name="building"),
    path("scenario/", views.scenario_view, name="scenario"),
    path("projects/", views.project_list_view, name="projects"),
    path("project/<int:project_id>/", views.project_detail_view, name="project_detail"),
    path("project/<int:project_id>/compare/", views.compare_scenarios_view, name="compare_scenarios"),
    path("project/<int:project_id>/add-scenario/", views.add_scenario_to_project_view, name="add_scenario_to_project"),
    path("project/<int:project_id>/delete/", views.delete_project_view, name="delete_project"),
    path("scenario/<int:scenario_id>/delete/", views.delete_scenario_view, name="delete_scenario"),
]
