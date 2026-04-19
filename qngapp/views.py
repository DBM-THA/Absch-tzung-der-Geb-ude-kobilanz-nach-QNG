from django.shortcuts import render


def calculate_qng(qng_level, construction_type, heating_system, ventilation_system, pv_area, battery_storage, garage):
    gwp = 24.0
    qpne = 96.0
    notes = []

    if construction_type == "holz":
        gwp -= 2.5
        qpne -= 4
        notes.append("Holzbauweise verbessert die Ökobilanz im Vergleich zur Massivbauweise.")
    else:
        notes.append("Massivbauweise wird als Referenzvariante verwendet.")

    if heating_system == "waermepumpe":
        gwp -= 1.5
        qpne -= 8
        notes.append("Wärmepumpe reduziert den Primärenergiebedarf.")
    elif heating_system == "fernwaerme":
        gwp -= 0.8
        qpne -= 4
        notes.append("Fernwärme verbessert die Werte moderat.")
    else:
        notes.append("Pellet / Nahwärme bleibt als Ausgangsannahme bestehen.")

    if ventilation_system == "wrg":
        qpne -= 3
        notes.append("Lüftung mit WRG verbessert die energetische Performance.")
    elif ventilation_system == "keine":
        qpne += 2
        notes.append("Ohne Lüftungsanlage wird der Wert leicht verschlechtert.")

    if pv_area > 0:
        pv_bonus = min(pv_area / 100, 5)
        gwp -= pv_bonus * 0.4
        qpne -= pv_bonus * 2
        notes.append("Die PV-Fläche verbessert die Ergebniswerte.")

    if battery_storage == "ja":
        gwp -= 0.6
        qpne -= 1.5
        notes.append("Ein Batteriespeicher bringt einen zusätzlichen kleinen Vorteil.")

    if garage == "ja":
        gwp += 1.2
        qpne += 2.5
        notes.append("Eine Tiefgarage verschlechtert die Bilanz in diesem einfachen Modell.")

    gwp = round(max(gwp, 0), 2)
    qpne = round(max(qpne, 0), 2)

    if qng_level == "plus":
        status_ok = gwp <= 24 and qpne <= 96
        status = "QNG-PLUS wird erfüllt." if status_ok else "QNG-PLUS wird aktuell nicht erfüllt."
    else:
        status_ok = gwp <= 20 and qpne <= 64
        status = "QNG-PREMIUM wird erfüllt." if status_ok else "QNG-PREMIUM wird aktuell nicht erfüllt."

    return {
        "gwp": gwp,
        "qpne": qpne,
        "status": status,
        "status_ok": status_ok,
        "notes": notes,
    }


def index(request):
    result = None
    form_data = {
        "project_name": "Mehrfamilienhaus Augsburg",
        "qng_level": "plus",
        "construction_type": "massiv",
        "heating_system": "pellet",
        "ventilation_system": "wrg",
        "pv_area": "300",
        "battery_storage": "nein",
        "garage": "nein",
    }

    if request.method == "POST":
        form_data = {
            "project_name": request.POST.get("project_name", ""),
            "qng_level": request.POST.get("qng_level", "plus"),
            "construction_type": request.POST.get("construction_type", "massiv"),
            "heating_system": request.POST.get("heating_system", "pellet"),
            "ventilation_system": request.POST.get("ventilation_system", "wrg"),
            "pv_area": request.POST.get("pv_area", "0"),
            "battery_storage": request.POST.get("battery_storage", "nein"),
            "garage": request.POST.get("garage", "nein"),
        }

        pv_area = float(form_data["pv_area"] or 0)

        result = calculate_qng(
            form_data["qng_level"],
            form_data["construction_type"],
            form_data["heating_system"],
            form_data["ventilation_system"],
            pv_area,
            form_data["battery_storage"],
            form_data["garage"],
        )
        result["project_name"] = form_data["project_name"] or "-"

    return render(request, "qngapp/index.html", {
        "result": result,
        "form_data": form_data,
    })