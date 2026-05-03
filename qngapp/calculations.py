# qngapp/calculations.py

from .qng_data import (
    KG300_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
)


def safe_float(value, default=0.0):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return default


def round2(value):
    return round(value, 2)


def calculate_kg300(building_type, nrf_total, nrf_tg):
    values = KG300_VALUES[building_type]
    relevant_area = max(nrf_total - nrf_tg, 0)

    return {
        "name": "Bauwerksteile KG 300",
        "ac_qp_abs": values["ac_qp_rel"] * relevant_area,
        "ac_gwp_abs": values["ac_gwp_rel"] * relevant_area,
        "d_qp_abs": values["d_qp_rel"] * relevant_area,
        "d_gwp_abs": values["d_gwp_rel"] * relevant_area,
        "ac_qp_rel": values["ac_qp_rel"],
        "ac_gwp_rel": values["ac_gwp_rel"],
        "d_qp_rel": values["d_qp_rel"],
        "d_gwp_rel": values["d_gwp_rel"],
    }


def calculate_kg400_sockel(energy_standard, nrf_total):
    values = KG400_SOCKEL_VALUES[energy_standard]

    return {
        "name": "Bauwerksteile KG 400 - Sockelbetrag",
        "ac_qp_abs": values["ac_qp_rel"] * nrf_total,
        "ac_gwp_abs": values["ac_gwp_rel"] * nrf_total,
        "d_qp_abs": values["d_qp_rel"] * nrf_total,
        "d_gwp_abs": values["d_gwp_rel"] * nrf_total,
        "ac_qp_rel": values["ac_qp_rel"],
        "ac_gwp_rel": values["ac_gwp_rel"],
        "d_qp_rel": values["d_qp_rel"],
        "d_gwp_rel": values["d_gwp_rel"],
    }


def calculate_kg400_grossgeraete(heating, ventilation, nrf_total):
    heating_values = KG400_GROSSGERAETE_VALUES["heating"][heating]
    ventilation_values = KG400_GROSSGERAETE_VALUES["ventilation"][ventilation]
    elevator_values = KG400_GROSSGERAETE_VALUES["elevator"][
        "Fahrstuhl - Grundkomponenten"
    ]

    ac_qp_abs = (
        heating_values["ac_qp_abs"]
        + ventilation_values["ac_qp_abs"]
        + elevator_values["ac_qp_abs"]
    )
    ac_gwp_abs = (
        heating_values["ac_gwp_abs"]
        + ventilation_values["ac_gwp_abs"]
        + elevator_values["ac_gwp_abs"]
    )
    d_qp_abs = (
        heating_values["d_qp_abs"]
        + ventilation_values["d_qp_abs"]
        + elevator_values["d_qp_abs"]
    )
    d_gwp_abs = (
        heating_values["d_gwp_abs"]
        + ventilation_values["d_gwp_abs"]
        + elevator_values["d_gwp_abs"]
    )

    return {
        "name": "Bauwerksteile KG 400 - Großgeräte",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": d_qp_abs,
        "d_gwp_abs": d_gwp_abs,
        "ac_qp_rel": ac_qp_abs / nrf_total if nrf_total else 0,
        "ac_gwp_rel": ac_gwp_abs / nrf_total if nrf_total else 0,
        "d_qp_rel": d_qp_abs / nrf_total if nrf_total else 0,
        "d_gwp_rel": d_gwp_abs / nrf_total if nrf_total else 0,
    }


def calculate_qng_result(
    nrf_total,
    nrf_tg,
    building_type,
    energy_standard,
    heating,
    ventilation,
    qng_level,
):
    nrf_total = safe_float(nrf_total)
    nrf_tg = safe_float(nrf_tg)

    kg300 = calculate_kg300(building_type, nrf_total, nrf_tg)
    kg400_sockel = calculate_kg400_sockel(energy_standard, nrf_total)
    kg400_gross = calculate_kg400_grossgeraete(heating, ventilation, nrf_total)

    parts = [kg300, kg400_sockel, kg400_gross]

    total_ac_qp_rel = sum(part["ac_qp_rel"] for part in parts)
    total_ac_gwp_rel = sum(part["ac_gwp_rel"] for part in parts)
    total_d_qp_rel = sum(part["d_qp_rel"] for part in parts)
    total_d_gwp_rel = sum(part["d_gwp_rel"] for part in parts)

    limits = QNG_LIMITS[qng_level]

    return {
        "inputs": {
            "nrf_total": nrf_total,
            "nrf_tg": nrf_tg,
            "building_type": building_type,
            "energy_standard": energy_standard,
            "heating": heating,
            "ventilation": ventilation,
            "qng_level": qng_level,
        },
        "parts": parts,
        "total": {
            "ac_qp_rel": round2(total_ac_qp_rel),
            "ac_gwp_rel": round2(total_ac_gwp_rel),
            "d_qp_rel": round2(total_d_qp_rel),
            "d_gwp_rel": round2(total_d_gwp_rel),
            "qp_limit": limits["qp"],
            "gwp_limit": limits["gwp"],
            "qp_status": "erfüllt" if total_ac_qp_rel <= limits["qp"] else "nicht erfüllt",
            "gwp_status": "erfüllt" if total_ac_gwp_rel <= limits["gwp"] else "nicht erfüllt",
        },
    }
