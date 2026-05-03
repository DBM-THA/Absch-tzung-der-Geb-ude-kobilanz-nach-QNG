from django.shortcuts import render

from .calculations import calculate_qng_result
from .qng_data import (
    KG300_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
)


def index(request):
    context = {
        "building_types": KG300_VALUES.keys(),
        "energy_standards": KG400_SOCKEL_VALUES.keys(),
        "heating_systems": KG400_GROSSGERAETE_VALUES["heating"].keys(),
        "ventilation_systems": KG400_GROSSGERAETE_VALUES["ventilation"].keys(),
        "qng_levels": QNG_LIMITS.keys(),
        "result": None,
    }

    if request.method == "POST":
        result = calculate_qng_result(
            nrf_total=request.POST.get("nrf_total", "5282"),
            nrf_tg=request.POST.get("nrf_tg", "0"),
            building_type=request.POST.get("building_type"),
            energy_standard=request.POST.get("energy_standard"),
            heating=request.POST.get("heating"),
            ventilation=request.POST.get("ventilation"),
            qng_level=request.POST.get("qng_level"),
        )
        context["result"] = result

    return render(request, "qngapp/index.html", context)
