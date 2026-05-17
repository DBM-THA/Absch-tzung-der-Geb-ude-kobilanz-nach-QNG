from django.contrib import admin

from .models import Building, Scenario


# ===== ADMIN TITEL =====

admin.site.site_header = "QNG Admin"
admin.site.site_title = "QNG Backend"
admin.site.index_title = "Projektverwaltung"


# ===== BUILDING ADMIN =====

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):

    list_display = (
        "project_name",
        "building_type",
        "energy_standard",
        "nrf_total",
        "nrf_heated",
        "an_geg",
    )

    search_fields = (
        "project_name",
    )

    list_filter = (
        "building_type",
        "energy_standard",
    )

    ordering = (
        "project_name",
    )


# ===== SCENARIO ADMIN =====

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):

    list_display = (
        "heating",
        "ventilation",
        "qng_level",
        "pv_area",
        "battery_storage",
    )

    list_filter = (
        "qng_level",
        "battery_storage",
        "heating",
    )

    ordering = (
        "qng_level",
    )
