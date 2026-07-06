from io import BytesIO
from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

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

    scenarios = (
        building.scenarios
        .all()
        .select_related("result")
        .order_by("created_at")
    )

    valid_scenarios = [
        scenario for scenario in scenarios
        if hasattr(scenario, "result")
    ]

    ranking = sorted(
        valid_scenarios,
        key=lambda scenario: (
            scenario.result.ac_qp_rel + scenario.result.ac_gwp_rel
        )
    )

    best_scenario = ranking[0] if ranking else None

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#0f2f26"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1f7a4d"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1a2e26"),
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#4b5563"),
    )

    story = []

    story.append(Paragraph("QNG-Check", title_style))
    story.append(Paragraph("Projektbericht zur Abschaetzung der Gebaeudeoekobilanz", subtitle_style))

    intro_data = [
        ["Projekt", building.project_name],
        ["Gebaeudeart", building.building_category],
        ["Bauweise", building.building_type],
        ["Energiestandard", building.energy_standard],
        ["NRF gesamt", f"{building.nrf_total:.2f} m2"],
        ["NRF beheizt", f"{building.nrf_heated:.2f} m2"],
        ["Tiefgarage", f"{building.nrf_tg:.2f} m2"],
        ["A_n nach GEG", f"{building.an_geg:.2f} m2"],
    ]

    project_table = Table(
        intro_data,
        colWidths=[4.2 * cm, 12.0 * cm],
        hAlign="LEFT",
    )

    project_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#dcfce7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#166534")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(Paragraph("Projektdaten", heading_style))
    story.append(project_table)
    story.append(Spacer(1, 12))

    if best_scenario:
        best_status = (
            "erfuellt"
            if best_scenario.result.qp_status == "erfüllt"
            and best_scenario.result.gwp_status == "erfüllt"
            else "nicht erfuellt"
        )

        story.append(Paragraph("Beste Variante", heading_style))

        best_data = [
            [
                Paragraph("<b>Szenario</b>", normal_style),
                Paragraph("<b>QP,ne</b>", normal_style),
                Paragraph("<b>GWP</b>", normal_style),
                Paragraph("<b>Status</b>", normal_style),
            ],
            [
                f"ID {best_scenario.id}",
                f"{best_scenario.result.ac_qp_rel:.2f}",
                f"{best_scenario.result.ac_gwp_rel:.2f}",
                best_status,
            ],
            [
                Paragraph("<b>Heizung</b>", normal_style),
                Paragraph(best_scenario.heating, normal_style),
                Paragraph("<b>Lueftung</b>", normal_style),
                Paragraph(best_scenario.ventilation, normal_style),
            ],
        ]

        best_table = Table(
            best_data,
            colWidths=[3.2 * cm, 3.2 * cm, 3.2 * cm, 6.8 * cm],
            hAlign="LEFT",
        )

        best_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a4d")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#dcfce7")),
            ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f9fafb")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))

        story.append(best_table)
        story.append(Spacer(1, 12))

    story.append(Paragraph("Szenarioueberblick", heading_style))

    scenario_data = [
        [
            "Rang",
            "ID",
            "Heizung",
            "Lueftung",
            "PV",
            "Batterie",
            "QNG",
            "QP,ne",
            "GWP",
            "Status",
        ]
    ]

    for index, scenario in enumerate(ranking, start=1):
        result = getattr(scenario, "result", None)

        if result:
            status = (
                "erfuellt"
                if result.qp_status == "erfüllt"
                and result.gwp_status == "erfüllt"
                else "nicht erfuellt"
            )

            scenario_data.append([
                str(index),
                str(scenario.id),
                Paragraph(scenario.heating, small_style),
                Paragraph(scenario.ventilation, small_style),
                f"{scenario.pv_area:.0f}",
                scenario.battery_storage,
                scenario.qng_level,
                f"{result.ac_qp_rel:.2f}",
                f"{result.ac_gwp_rel:.2f}",
                status,
            ])

    if len(scenario_data) == 1:
        scenario_data.append(["-", "-", "kein Ergebnis", "-", "-", "-", "-", "-", "-", "-"])

    scenario_table = Table(
        scenario_data,
        colWidths=[
            1.0 * cm,
            0.9 * cm,
            3.0 * cm,
            3.0 * cm,
            1.0 * cm,
            1.4 * cm,
            1.7 * cm,
            1.3 * cm,
            1.3 * cm,
            1.8 * cm,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f7a4d")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#d1d5db")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]

    for row_index in range(1, len(scenario_data)):
        if row_index % 2 == 0:
            table_style.append(
                ("BACKGROUND", (0, row_index), (-1, row_index), colors.HexColor("#f9fafb"))
            )

    if len(scenario_data) > 1:
        table_style.append(
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#dcfce7"))
        )
        table_style.append(
            ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#166534"))
        )
        table_style.append(
            ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold")
        )

    scenario_table.setStyle(TableStyle(table_style))
    story.append(scenario_table)

    story.append(Spacer(1, 14))
    story.append(Paragraph("Kurzfazit", heading_style))

    if best_scenario:
        story.append(Paragraph(
            f"Fuer das Projekt wurden {len(valid_scenarios)} Szenarien mit Ergebniswerten untersucht. "
            f"Die aktuell beste Variante ist Szenario ID {best_scenario.id}. "
            f"Sie erreicht einen QP,ne-Wert von {best_scenario.result.ac_qp_rel:.2f} "
            f"und einen GWP-Wert von {best_scenario.result.ac_gwp_rel:.2f}.",
            normal_style,
        ))
    else:
        story.append(Paragraph(
            "Fuer dieses Projekt liegen noch keine auswertbaren Szenarioergebnisse vor.",
            normal_style,
        ))

    story.append(Spacer(1, 18))
    story.append(Paragraph(
        "Erstellt mit QNG-Check - Technische Hochschule Augsburg - Digitaler Baumeister",
        small_style,
    ))

    document.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="qng_bericht.pdf"'
    response["Content-Length"] = str(len(pdf))

    return response
