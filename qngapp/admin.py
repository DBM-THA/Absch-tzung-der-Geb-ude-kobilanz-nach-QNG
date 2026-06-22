from django.contrib import admin

from .models import Building, Scenario, Result


admin.site.site_header = "QNG Admin"
admin.site.site_title = "QNG Backend"
admin.site.index_title = "Projektverwaltung"


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "project_name",
        "building_type",
        "energy_standard",
        "nrf_total",
        "nrf_heated",
        "an_geg",
        "created_at",
    )

    search_fields = ("project_name",)
    list_filter = ("building_type", "energy_standard")
    ordering = ("-created_at",)


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = (
        "building",
        "heating",
        "ventilation",
        "qng_level",
        "pv_area",
        "battery_storage",
        "created_at",
    )

    list_filter = (
        "qng_level",
        "battery_storage",
        "heating",
        "ventilation",
    )

    search_fields = (
        "building__project_name",
        "heating",
        "ventilation",
    )

    ordering = ("-created_at",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "scenario",
        "ac_qp_rel",
        "ac_gwp_rel",
        "qp_limit",
        "gwp_limit",
        "qp_status",
        "gwp_status",
        "created_at",
    )

    list_filter = (
        "qp_status",
        "gwp_status",
    )

    search_fields = (
        "scenario__building__project_name",
        "scenario__qng_level",
    )

    ordering = ("-created_at",)
