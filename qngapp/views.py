from django.shortcuts import render, redirect

from .calculations import calculate_qng_result
from .qng_data import (
    KG300_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
)


def building_view(request):
    if request.method == "POST":
        request.session["building_data"] = {
            "project_name": request.POST.get("project_name", "Beispielgebäude"),
            "nrf_total": request.POST.get("nrf_total", "5282"),
            "nrf_tg": request.POST.get("nrf_tg", "0"),
            "nrf_heated": request.POST.get("nrf_heated", request.POST.get("nrf_total", "5282")),
            "an_geg": request.POST.get("an_geg", "6201"),
            "building_type": request.POST.get("building_type"),
            "energy_standard": request.POST.get("energy_standard"),
        }
        return redirect("scenario")

    return render(request, "qngapp/building.html", {
        "building_types": KG300_VALUES.keys(),
        "energy_standards": KG400_SOCKEL_VALUES.keys(),
    })


def scenario_view(request):
    building_data = request.session.get("building_data")

    if not building_data:
        return redirect("building")

    result = None

    if request.method == "POST":
        result = calculate_qng_result(
            nrf_total=building_data["nrf_total"],
            nrf_tg=building_data["nrf_tg"],
            nrf_heated=building_data["nrf_heated"],
            an_geg=building_data["an_geg"],
            building_type=building_data["building_type"],
            energy_standard=building_data["energy_standard"],
            heating=request.POST.get("heating"),
            ventilation=request.POST.get("ventilation"),
            qng_level=request.POST.get("qng_level"),
            pv_area=request.POST.get("pv_area", "0"),
            battery_storage=request.POST.get("battery_storage", "nein"),
        )

    return render(request, "qngapp/scenario.html", {
        "building": building_data,
        "heating_systems": KG400_GROSSGERAETE_VALUES["heating"].keys(),
        "ventilation_systems": KG400_GROSSGERAETE_VALUES["ventilation"].keys(),
        "qng_levels": QNG_LIMITS.keys(),
        "result": result,
    })
