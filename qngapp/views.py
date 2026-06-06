from django.shortcuts import render, redirect, get_object_or_404

from .calculations import calculate_qng_result
from .models import Building, Scenario, Result
from .qng_data import (
    KG300_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
)


def to_float(value, default=0):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return default


def building_view(request):
    an_geg_warning = None

    if request.method == "POST":
        nrf_heated_raw = request.POST.get("nrf_heated", "5282")
        nrf_tg_raw = request.POST.get("nrf_tg", "0")
        an_geg_raw = request.POST.get("an_geg", "6201")

        nrf_heated = to_float(nrf_heated_raw)
        nrf_tg = to_float(nrf_tg_raw)
        an_geg = to_float(an_geg_raw)

        nrf_total = nrf_heated + nrf_tg

        if an_geg < nrf_heated:
            an_geg_warning = (
                "Die Energiebezugsfläche Aₙ sollte normalerweise größer "
                "als die beheizte Nettogrundfläche sein."
            )

            return render(request, "qngapp/building.html", {
                "building_types": KG300_VALUES.keys(),
                "energy_standards": KG400_SOCKEL_VALUES.keys(),
                "an_geg_warning": an_geg_warning,
                "form_data": {
                    "project_name": request.POST.get("project_name", "Beispielgebäude"),
                    "nrf_tg": nrf_tg_raw,
                    "nrf_heated": nrf_heated_raw,
                    "an_geg": an_geg_raw,
                    "building_type": request.POST.get("building_type"),
                    "energy_standard": request.POST.get("energy_standard"),
                },
            })

        building = Building.objects.create(
            project_name=request.POST.get("project_name", "Beispielgebäude"),
            nrf_total=nrf_total,
            nrf_tg=nrf_tg,
            nrf_heated=nrf_heated,
            an_geg=an_geg,
            building_type=request.POST.get("building_type"),
            energy_standard=request.POST.get("energy_standard"),
        )

        request.session["building_id"] = building.id

        return redirect("scenario")

    return render(request, "qngapp/building.html", {
        "building_types": KG300_VALUES.keys(),
        "energy_standards": KG400_SOCKEL_VALUES.keys(),
        "an_geg_warning": an_geg_warning,
        "form_data": {
            "project_name": "Beispielgebäude",
            "nrf_tg": "0",
            "nrf_heated": "5282",
            "an_geg": "6201",
        },
    })


def scenario_view(request):
    building_id = request.session.get("building_id")

    if not building_id:
        return redirect("building")

    building = get_object_or_404(Building, id=building_id)

    scenario_data = request.session.get("scenario_data", {
        "heating": "Nahwärme, Pelletkessel",
        "ventilation": "Zu-/Abluftanlage mit WRG",
        "pv_area": "300",
        "battery_storage": "nein",
        "qng_level": "QNG-PLUS",
    })

    if request.method == "POST":
        scenario_data = {
            "heating": request.POST.get("heating"),
            "ventilation": request.POST.get("ventilation"),
            "pv_area": request.POST.get("pv_area", "300"),
            "battery_storage": request.POST.get("battery_storage", "nein"),
            "qng_level": request.POST.get("qng_level"),
        }

        request.session["scenario_data"] = scenario_data

    result = calculate_qng_result(
        nrf_total=building.nrf_total,
        nrf_tg=building.nrf_tg,
        nrf_heated=building.nrf_heated,
        an_geg=building.an_geg,
        building_type=building.building_type,
        energy_standard=building.energy_standard,
        heating=scenario_data["heating"],
        ventilation=scenario_data["ventilation"],
        qng_level=scenario_data["qng_level"],
        pv_area=scenario_data["pv_area"],
        battery_storage=scenario_data["battery_storage"],
    )

    if request.method == "POST":
        scenario = Scenario.objects.create(
            building=building,
            heating=scenario_data["heating"],
            ventilation=scenario_data["ventilation"],
            pv_area=to_float(scenario_data["pv_area"]),
            battery_storage=scenario_data["battery_storage"],
            qng_level=scenario_data["qng_level"],
        )

        Result.objects.create(
            scenario=scenario,
            ac_qp_rel=result["total"]["ac_qp_rel"],
            ac_gwp_rel=result["total"]["ac_gwp_rel"],
            qp_limit=result["total"]["qp_limit"],
            gwp_limit=result["total"]["gwp_limit"],
            qp_status=result["total"]["qp_status"],
            gwp_status=result["total"]["gwp_status"],
        )

    building_data = {
        "project_name": building.project_name,
        "nrf_total": building.nrf_total,
        "nrf_tg": building.nrf_tg,
        "nrf_heated": building.nrf_heated,
        "an_geg": building.an_geg,
        "building_type": building.building_type,
        "energy_standard": building.energy_standard,
    }

    return render(request, "qngapp/scenario.html", {
        "building": building_data,
        "scenario": scenario_data,
        "heating_systems": KG400_GROSSGERAETE_VALUES["heating"].keys(),
        "ventilation_systems": KG400_GROSSGERAETE_VALUES["ventilation"].keys(),
        "qng_levels": QNG_LIMITS.keys(),
        "result": result,
    })
def project_list_view(request):
    projects = Building.objects.all().order_by("-created_at")

    return render(
        request,
        "qngapp/projects.html",
        {
            "projects": projects,
        },
    )
