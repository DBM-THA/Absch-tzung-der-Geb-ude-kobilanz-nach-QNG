# qngapp/calculations.py

import math

from .qng_data import (
    KG300_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
    END_ENERGY_BASE_AN_GEG,
    END_ENERGY_DEMANDS,
    ENERGY_FACTORS,
    DEFAULT_ENERGY_CARRIERS,
    USER_ELECTRICITY_KWH_PER_M2,
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


def calculate_b6_1a(ventilation, heating, an_geg, nrf_total):
    base = END_ENERGY_DEMANDS[(ventilation, heating)]
    scale = an_geg / END_ENERGY_BASE_AN_GEG if END_ENERGY_BASE_AN_GEG else 1

    heating_kwh = base["heating"] * scale
    hot_water_kwh = base["hot_water"] * scale
    auxiliary_kwh = base["auxiliary"] * scale

    heating_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["heating"]]
    hot_water_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["hot_water"]]
    auxiliary_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["auxiliary"]]

    qp_abs = (
        heating_kwh * heating_factor["qp"]
        + hot_water_kwh * hot_water_factor["qp"]
        + auxiliary_kwh * auxiliary_factor["qp"]
    )

    gwp_abs = (
        heating_kwh * heating_factor["gwp"]
        + hot_water_kwh * hot_water_factor["gwp"]
        + auxiliary_kwh * auxiliary_factor["gwp"]
    )

    return {
        "name": "B6.1a Energiebedarf",
        "ac_qp_abs": qp_abs,
        "ac_gwp_abs": gwp_abs,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": qp_abs / nrf_total if nrf_total else 0,
        "ac_gwp_rel": gwp_abs / nrf_total if nrf_total else 0,
        "d_qp_rel": 0,
        "d_gwp_rel": 0,
    }


def calculate_nutzerstrom(nrf_heated, nrf_total):
    electricity_kwh = USER_ELECTRICITY_KWH_PER_M2 * nrf_heated
    factor = ENERGY_FACTORS["Nutzung - 1 kWh nationaler Netzstrommix"]

    qp_abs = electricity_kwh * factor["qp"]
    gwp_abs = electricity_kwh * factor["gwp"]

    return {
        "name": "B6.3 Nutzerstrom",
        "ac_qp_abs": qp_abs,
        "ac_gwp_abs": gwp_abs,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": qp_abs / nrf_total if nrf_total else 0,
        "ac_gwp_rel": gwp_abs / nrf_total if nrf_total else 0,
        "d_qp_rel": 0,
        "d_gwp_rel": 0,
    }


def calculate_pv(pv_area, battery_storage, nrf_total):
    pv_area = safe_float(pv_area)

    if pv_area <= 0:
        pv_parts_qp = 0
        pv_parts_gwp = 0
        pv_d_qp = 0
        pv_d_gwp = 0
        b6_qp = 0
        b6_gwp = 0
        d2_qp = 0
        d2_gwp = 0

    elif pv_area < 300:
        pv_parts_qp = 12600 * (1 - math.exp(-0.0061 * pv_area))
        pv_parts_gwp = 3515 * (1 - math.exp(-0.0061 * pv_area))

        pv_d_qp = -2.0931 * pv_area
        pv_d_gwp = -0.6792 * pv_area

        b6_qp = -222.58 * pv_area
        b6_gwp = -63.608 * pv_area

        d2_qp = 0
        d2_gwp = 0

    else:
        if battery_storage == "ja":
            pv_parts_qp = 41125 * (1 - math.exp(-0.0023 * (pv_area - 89.72)))
            pv_parts_gwp = 11425 * (1 - math.exp(-0.0023 * (pv_area - 89.11)))

            pv_d_qp = -2027 * (1 - math.exp(-0.0022 * (pv_area - 72.7)))
            pv_d_gwp = -639 * (1 - math.exp(-0.0022 * (pv_area - 72.21)))

            b6_qp = -184610 * (1 - math.exp(-0.0022 * (pv_area - 61.27)))
            b6_gwp = -52760 * (1 - math.exp(-0.0022 * (pv_area - 61.26)))

            d2_qp = -0.0202 * pv_area**2 - 20.884 * pv_area + 9533.1
            d2_gwp = -0.0137 * pv_area**2 - 14.148 * pv_area + 6458.2

        else:
            pv_parts_qp = 12600 * (1 - math.exp(-0.0061 * pv_area))
            pv_parts_gwp = 3515 * (1 - math.exp(-0.0061 * pv_area))

            pv_d_qp = -635 * (1 - math.exp(-0.0061 * pv_area))
            pv_d_gwp = -206 * (1 - math.exp(-0.0061 * pv_area))

            b6_qp = -70065 + 3172.11 * math.exp(-0.011 * (pv_area - 303.36))
            b6_gwp = -20025 + 842.39 * math.exp(-0.0108 * (pv_area - 310.42))

            d2_qp = -87.72 * pv_area + 24860
            d2_gwp = -60.781 * pv_area + 16841

    return {
        "pv_parts": {
            "name": "Bauwerksteile Photovoltaik",
            "ac_qp_abs": pv_parts_qp,
            "ac_gwp_abs": pv_parts_gwp,
            "d_qp_abs": pv_d_qp,
            "d_gwp_abs": pv_d_gwp,
            "ac_qp_rel": pv_parts_qp / nrf_total if nrf_total else 0,
            "ac_gwp_rel": pv_parts_gwp / nrf_total if nrf_total else 0,
            "d_qp_rel": pv_d_qp / nrf_total if nrf_total else 0,
            "d_gwp_rel": pv_d_gwp / nrf_total if nrf_total else 0,
        },
        "b6_1b": {
            "name": "B6.1b eigengenutzter PV-Strom",
            "ac_qp_abs": b6_qp,
            "ac_gwp_abs": b6_gwp,
            "d_qp_abs": 0,
            "d_gwp_abs": 0,
            "ac_qp_rel": b6_qp / nrf_total if nrf_total else 0,
            "ac_gwp_rel": b6_gwp / nrf_total if nrf_total else 0,
            "d_qp_rel": 0,
            "d_gwp_rel": 0,
        },
        "d2": {
            "name": "Modul D2 Energieexport",
            "d_qp_abs": d2_qp,
            "d_gwp_abs": d2_gwp,
            "d_qp_rel": d2_qp / nrf_total if nrf_total else 0,
            "d_gwp_rel": d2_gwp / nrf_total if nrf_total else 0,
        },
    }


def calculate_qng_result(
    nrf_total,
    nrf_tg,
    building_type,
    energy_standard,
    heating,
    ventilation,
    qng_level,
    an_geg=6201,
    nrf_heated=None,
    pv_area=0,
    battery_storage="nein",
):
    nrf_total = safe_float(nrf_total)
    nrf_tg = safe_float(nrf_tg)
    an_geg = safe_float(an_geg)

    if nrf_heated is None:
        nrf_heated = nrf_total
    else:
        nrf_heated = safe_float(nrf_heated, nrf_total)

    kg300 = calculate_kg300(building_type, nrf_total, nrf_tg)
    kg400_sockel = calculate_kg400_sockel(energy_standard, nrf_total)
    kg400_gross = calculate_kg400_grossgeraete(heating, ventilation, nrf_total)

    pv = calculate_pv(pv_area, battery_storage, nrf_total)
    b6_1a = calculate_b6_1a(ventilation, heating, an_geg, nrf_total)
    nutzerstrom = calculate_nutzerstrom(nrf_heated, nrf_total)

    parts = [
        kg300,
        kg400_sockel,
        kg400_gross,
        pv["pv_parts"],
        b6_1a,
        pv["b6_1b"],
        nutzerstrom,
    ]

    total_ac_qp_rel = sum(part["ac_qp_rel"] for part in parts)
    total_ac_gwp_rel = sum(part["ac_gwp_rel"] for part in parts)

    total_d_qp_rel = sum(part["d_qp_rel"] for part in parts) + pv["d2"]["d_qp_rel"]
    total_d_gwp_rel = sum(part["d_gwp_rel"] for part in parts) + pv["d2"]["d_gwp_rel"]

    total_ac_qp_abs = sum(part["ac_qp_abs"] for part in parts)
    total_ac_gwp_abs = sum(part["ac_gwp_abs"] for part in parts)

    total_d_qp_abs = sum(part["d_qp_abs"] for part in parts) + pv["d2"]["d_qp_abs"]
    total_d_gwp_abs = sum(part["d_gwp_abs"] for part in parts) + pv["d2"]["d_gwp_abs"]

    limits = QNG_LIMITS[qng_level]

    return {
        "inputs": {
            "nrf_total": nrf_total,
            "nrf_tg": nrf_tg,
            "nrf_heated": nrf_heated,
            "an_geg": an_geg,
            "building_type": building_type,
            "energy_standard": energy_standard,
            "heating": heating,
            "ventilation": ventilation,
            "qng_level": qng_level,
            "pv_area": safe_float(pv_area),
            "battery_storage": battery_storage,
        },
        "parts": parts,
        "module_d2": pv["d2"],
        "total": {
            "ac_qp_abs": round2(total_ac_qp_abs),
            "ac_gwp_abs": round2(total_ac_gwp_abs),
            "d_qp_abs": round2(total_d_qp_abs),
            "d_gwp_abs": round2(total_d_gwp_abs),
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
