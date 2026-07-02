from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
    project_name_warning = None

    if request.method == "POST":
        project_name = request.POST.get("project_name", "Beispielgebäude").strip()
        building_category = request.POST.get("building_category", "Mehrfamilienhaus")

        nrf_heated_raw = request.POST.get("nrf_heated", "5282")
        nrf_tg_raw = request.POST.get("nrf_tg", "0")
        an_geg_raw = request.POST.get("an_geg", "6201")

        nrf_heated = to_float(nrf_heated_raw)
        nrf_tg = to_float(nrf_tg_raw)
        an_geg = to_float(an_geg_raw)

        nrf_total = nrf_heated + nrf_tg

        if Building.objects.filter(project_name__iexact=project_name).exists():
            project_name_warning = (
                "Ein Projekt mit diesem Namen existiert bereits. "
                "Bitte wählen Sie einen anderen Projektnamen."
            )

            return render(request, "qngapp/building.html", {
                "building_types": KG300_VALUES.keys(),
                "energy_standards": KG400_SOCKEL_VALUES.keys(),
                "an_geg_warning": an_geg_warning,
                "project_name_warning": project_name_warning,
                "form_data": {
                    "project_name": project_name,
                    "building_category": building_category,
                    "nrf_tg": nrf_tg_raw,
                    "nrf_heated": nrf_heated_raw,
                    "an_geg": an_geg_raw,
                    "building_type": request.POST.get("building_type"),
                    "energy_standard": request.POST.get("energy_standard"),
                },
            })

        if an_geg < nrf_heated:
            an_geg_warning = (
                "Die Energiebezugsfläche Aₙ sollte normalerweise größer "
                "als die beheizte Nettogrundfläche sein."
            )

            return render(request, "qngapp/building.html", {
                "building_types": KG300_VALUES.keys(),
                "energy_standards": KG400_SOCKEL_VALUES.keys(),
                "an_geg_warning": an_geg_warning,
                "project_name_warning": project_name_warning,
                "form_data": {
                    "project_name": request.POST.get("project_name", "Beispielgebäude"),
                    "building_category": request.POST.get("building_category", "Mehrfamilienhaus"),
                    "nrf_tg": nrf_tg_raw,
                    "nrf_heated": nrf_heated_raw,
                    "an_geg": an_geg_raw,
                    "building_type": request.POST.get("building_type"),
                    "energy_standard": request.POST.get("energy_standard"),
                },
            })

        building = Building.objects.create(
            project_name=project_name,
            building_category=building_category,
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
        "project_name_warning": project_name_warning,
        "form_data": {
            "project_name": "Mehrfamilienhaus Nürnberg",
            "building_category": "Mehrfamilienhaus",
            "nrf_tg": "0",
            "nrf_heated": "5282",
            "an_geg": "6201",
        },
    })


def scenario_view(request):
    building_id = request.session.get("building_id")

    if not building_id:
        return redirect("building")

    building = Building.objects.filter(id=building_id).first()

    if not building:
        request.session.pop("building_id", None)
        request.session.pop("scenario_data", None)
        return redirect("building")

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
        scenario = Scenario.objects.filter(
            building=building,
            heating=scenario_data["heating"],
            ventilation=scenario_data["ventilation"],
            pv_area=to_float(scenario_data["pv_area"]),
            battery_storage=scenario_data["battery_storage"],
            qng_level=scenario_data["qng_level"],
        ).first()

        if not scenario:
            scenario = Scenario.objects.create(
                building=building,
                heating=scenario_data["heating"],
                ventilation=scenario_data["ventilation"],
                pv_area=to_float(scenario_data["pv_area"]),
                battery_storage=scenario_data["battery_storage"],
                qng_level=scenario_data["qng_level"],
            )

        Result.objects.update_or_create(
            scenario=scenario,
            defaults={
                "ac_qp_rel": result["total"]["ac_qp_rel"],
                "ac_gwp_rel": result["total"]["ac_gwp_rel"],
                "qp_limit": result["total"]["qp_limit"],
                "gwp_limit": result["total"]["gwp_limit"],
                "qp_status": result["total"]["qp_status"],
                "gwp_status": result["total"]["gwp_status"],
            }
        )

    building_data = {
        "project_name": building.project_name,
        "building_category": building.building_category,
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

    return render(request, "qngapp/projects.html", {
        "projects": projects,
    })


def project_detail_view(request, project_id):
    building = Building.objects.filter(id=project_id).first()

    if not building:
        return redirect("building")

    scenarios = building.scenarios.all().order_by("-created_at")

    return render(request, "qngapp/project_detail.html", {
        "building": building,
        "scenarios": scenarios,
    })


def compare_scenarios_view(request, project_id):
    building = Building.objects.filter(id=project_id).first()

    if not building:
        return redirect("building")

    scenario_ids = request.GET.getlist("scenario_ids")

    scenarios = (
        Scenario.objects
        .filter(id__in=scenario_ids, building=building)
        .select_related("result")
        .order_by("created_at")
    )

    valid_scenarios = [
        scenario for scenario in scenarios
        if hasattr(scenario, "result")
    ]

    best_qp = min(
        [scenario.result.ac_qp_rel for scenario in valid_scenarios],
        default=None
    )

    best_gwp = min(
        [scenario.result.ac_gwp_rel for scenario in valid_scenarios],
        default=None
    )

    ranking = sorted(
        valid_scenarios,
        key=lambda scenario: (
            scenario.result.ac_qp_rel + scenario.result.ac_gwp_rel
        )
    )

    best_scenario = ranking[0] if ranking else None

    return render(request, "qngapp/compare_scenarios.html", {
        "building": building,
        "scenarios": scenarios,
        "best_qp": best_qp,
        "best_gwp": best_gwp,
        "ranking": ranking,
        "best_scenario": best_scenario,
    })



def add_scenario_to_project_view(request, project_id):
    building = Building.objects.filter(id=project_id).first()

    if not building:
        return redirect("building")

    request.session["building_id"] = building.id
    request.session.pop("scenario_data", None)

    return redirect("scenario")

def delete_scenario_view(request, scenario_id):
    scenario = Scenario.objects.filter(id=scenario_id).first()

    if not scenario:
        return redirect("projects")

    building_id = scenario.building.id

    if request.method == "POST":
        scenario.delete()

    return redirect("project_detail", project_id=building_id)


def delete_project_view(request, project_id):
    project = Building.objects.filter(id=project_id).first()

    if not project:
        return redirect("projects")

    if request.method == "POST":
        project.delete()

        request.session.pop("building_id", None)
        request.session.pop("scenario_data", None)

    return redirect("projects")

def export_project_pdf_view(request, project_id):
    building = Building.objects.filter(id=project_id).first()

    if not building:
        return redirect("projects")

    scenarios = building.scenarios.all().select_related("result")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{building.project_name}_QNG_Bericht.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "QNG-Check Bericht")

    y -= 35
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Projektdaten")

    y -= 25
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Projektname: {building.project_name}")
    y -= 18
    p.drawString(50, y, f"Gebäudeart: {building.building_category}")
    y -= 18
    p.drawString(50, y, f"Bauweise: {building.building_type}")
    y -= 18
    p.drawString(50, y, f"Energiestandard: {building.energy_standard}")
    y -= 18
    p.drawString(50, y, f"NRF gesamt: {building.nrf_total} m²")
    y -= 18
    p.drawString(50, y, f"A_n nach GEG: {building.an_geg} m²")

    y -= 35
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Gespeicherte Szenarien")

    y -= 25
    p.setFont("Helvetica-Bold", 9)
    p.drawString(50, y, "ID")
    p.drawString(80, y, "Heizung")
    p.drawString(220, y, "PV")
    p.drawString(270, y, "QNG")
    p.drawString(350, y, "QP,ne")
    p.drawString(410, y, "GWP")
    p.drawString(470, y, "Status")

    y -= 15
    p.setFont("Helvetica", 8)

    for scenario in scenarios:
        if y < 60:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 8)

        result = getattr(scenario, "result", None)

        qp = result.ac_qp_rel if result else "-"
        gwp = result.ac_gwp_rel if result else "-"
        status = (
            f"{result.qp_status} / {result.gwp_status}"
            if result
            else "kein Ergebnis"
        )

        heating = scenario.heating[:22]

        p.drawString(50, y, str(scenario.id))
        p.drawString(80, y, heating)
        p.drawString(220, y, str(scenario.pv_area))
        p.drawString(270, y, scenario.qng_level)
        p.drawString(350, y, str(qp))
        p.drawString(410, y, str(gwp))
        p.drawString(470, y, status[:18])

        y -= 16

    p.showPage()
    p.save()

    return response
