# qngapp/calculations.py

import math

from .qng_data import (
    KG300_VALUES,
    KG300_TIEFGARAGE_VALUES,
    KG400_SOCKEL_VALUES,
    KG400_GROSSGERAETE_VALUES,
    QNG_LIMITS,
    END_ENERGY_BASE_AN_GEG,
    END_ENERGY_DEMANDS,
    ENERGY_FACTORS,
    DEFAULT_ENERGY_CARRIERS,
    USER_ELECTRICITY_KWH_PER_M2,
)


# ============================================================
# Hilfsfunktion
# ============================================================

def safe_divide(value, divisor):
    divisor = float(divisor)
    if divisor == 0:
        return 0
    return value / divisor


# ============================================================
# KG300
# ============================================================

def calculate_kg300(building_type, nrf_total, nrf_tg):
    values = KG300_VALUES[building_type]

    heated_area = max(float(nrf_total) - float(nrf_tg), 0)
    tg_area = max(float(nrf_tg), 0)

    ac_qp_abs = (
        values["ac_qp_rel"] * heated_area
        + KG300_TIEFGARAGE_VALUES["ac_qp_rel"] * tg_area
    )

    ac_gwp_abs = (
        values["ac_gwp_rel"] * heated_area
        + KG300_TIEFGARAGE_VALUES["ac_gwp_rel"] * tg_area
    )

    d_qp_abs = (
        values["d_qp_rel"] * heated_area
        + KG300_TIEFGARAGE_VALUES["d_qp_rel"] * tg_area
    )

    d_gwp_abs = (
        values["d_gwp_rel"] * heated_area
        + KG300_TIEFGARAGE_VALUES["d_gwp_rel"] * tg_area
    )

    return {
        "name": "Bauwerksteile KG300",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": d_qp_abs,
        "d_gwp_abs": d_gwp_abs,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": safe_divide(d_qp_abs, nrf_total),
        "d_gwp_rel": safe_divide(d_gwp_abs, nrf_total),
    }


# ============================================================
# KG400 Sockel
# ============================================================

def calculate_kg400_sockel(energy_standard):
    values = KG400_SOCKEL_VALUES[energy_standard]

    return {
        "name": "Bauwerksteile KG400 - Sockelbetrag",
        "ac_qp_abs": 0,
        "ac_gwp_abs": 0,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": values["ac_qp_rel"],
        "ac_gwp_rel": values["ac_gwp_rel"],
        "d_qp_rel": values["d_qp_rel"],
        "d_gwp_rel": values["d_gwp_rel"],
    }


# ============================================================
# KG400 Großgeräte
# ============================================================

def calculate_kg400_grossgeraete(heating, ventilation, nrf_total, nrf_tg):
    heated_area = max(float(nrf_total) - float(nrf_tg), 0)

    heating_values = KG400_GROSSGERAETE_VALUES["heating"][heating]
    ventilation_values = KG400_GROSSGERAETE_VALUES["ventilation"][ventilation]
    elevator_values = KG400_GROSSGERAETE_VALUES["elevator"][
        "Fahrstuhl - Grundkomponenten"
    ]

    ac_qp_abs = (
        heating_values["ac_qp_rel"]
        + ventilation_values["ac_qp_rel"]
        + elevator_values["ac_qp_rel"]
    ) * heated_area

    ac_gwp_abs = (
        heating_values["ac_gwp_rel"]
        + ventilation_values["ac_gwp_rel"]
        + elevator_values["ac_gwp_rel"]
    ) * heated_area

    d_qp_abs = (
        heating_values["d_qp_rel"]
        + ventilation_values["d_qp_rel"]
        + elevator_values["d_qp_rel"]
    ) * heated_area

    d_gwp_abs = (
        heating_values["d_gwp_rel"]
        + ventilation_values["d_gwp_rel"]
        + elevator_values["d_gwp_rel"]
    ) * heated_area

    return {
        "name": "Bauwerksteile KG400 - Großgeräte",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": d_qp_abs,
        "d_gwp_abs": d_gwp_abs,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": safe_divide(d_qp_abs, nrf_total),
        "d_gwp_rel": safe_divide(d_gwp_abs, nrf_total),
    }


# ============================================================
# B6.1a Energiebedarf
# ============================================================

def calculate_b6_1a(ventilation, heating, an_geg, nrf_total):
    demand = END_ENERGY_DEMANDS[(ventilation, heating)]
    scale_factor = float(an_geg) / END_ENERGY_BASE_AN_GEG

    heating_kwh = demand["heating"] * scale_factor
    hot_water_kwh = demand["hot_water"] * scale_factor
    auxiliary_kwh = demand["auxiliary"] * scale_factor

    heating_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["heating"]]
    hot_water_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["hot_water"]]
    auxiliary_factor = ENERGY_FACTORS[DEFAULT_ENERGY_CARRIERS["auxiliary"]]

    ac_qp_abs = (
        heating_kwh * heating_factor["qp"]
        + hot_water_kwh * hot_water_factor["qp"]
        + auxiliary_kwh * auxiliary_factor["qp"]
    )

    ac_gwp_abs = (
        heating_kwh * heating_factor["gwp"]
        + hot_water_kwh * hot_water_factor["gwp"]
        + auxiliary_kwh * auxiliary_factor["gwp"]
    )

    return {
        "name": "B6.1a - Betriebsenergie",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": 0,
        "d_gwp_rel": 0,
    }


# ============================================================
# B6.3 Nutzerstrom
# ============================================================

def calculate_user_electricity(nrf_total):
    electricity_kwh = USER_ELECTRICITY_KWH_PER_M2 * float(nrf_total)

    factor = ENERGY_FACTORS[
        "Nutzung - 1 kWh nationaler Netzstrommix"
    ]

    ac_qp_abs = electricity_kwh * factor["qp"]
    ac_gwp_abs = electricity_kwh * factor["gwp"]

    return {
        "name": "B6.3 - Nutzerstrom",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": 0,
        "d_gwp_rel": 0,
    }


# ============================================================
# Photovoltaik Bauteile
# ============================================================

def calculate_pv(
    pv_area,
    battery_storage,
    nrf_total,
):
    try:
        pv_area = float(str(pv_area).replace(",", "."))
    except (TypeError, ValueError):
        pv_area = 0

    if pv_area <= 0:
        return {
            "name": "Bauwerksteile Photovoltaik",
            "ac_qp_abs": 0,
            "ac_gwp_abs": 0,
            "d_qp_abs": 0,
            "d_gwp_abs": 0,
            "ac_qp_rel": 0,
            "ac_gwp_rel": 0,
            "d_qp_rel": 0,
            "d_gwp_rel": 0,
        }

    if pv_area < 300:
        ac_qp_abs = 12600 * (1 - math.exp(-0.0061 * pv_area))
        ac_gwp_abs = 3515 * (1 - math.exp(-0.0061 * pv_area))
        d_qp_abs = -2.0931 * pv_area
        d_gwp_abs = -0.6792 * pv_area

    else:
        if battery_storage == "ja":
            ac_qp_abs = 41125 * (
                1 - math.exp(-0.0023 * (pv_area - 89.72))
            )
            ac_gwp_abs = 11425 * (
                1 - math.exp(-0.0023 * (pv_area - 89.11))
            )
            d_qp_abs = -2027 * (
                1 - math.exp(-0.0022 * (pv_area - 72.7))
            )
            d_gwp_abs = -639 * (
                1 - math.exp(-0.0022 * (pv_area - 72.21))
            )
        else:
            ac_qp_abs = 12600 * (1 - math.exp(-0.0061 * pv_area))
            ac_gwp_abs = 3515 * (1 - math.exp(-0.0061 * pv_area))
            d_qp_abs = -635 * (1 - math.exp(-0.0061 * pv_area))
            d_gwp_abs = -206 * (1 - math.exp(-0.0061 * pv_area))

    return {
        "name": "Bauwerksteile Photovoltaik",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": d_qp_abs,
        "d_gwp_abs": d_gwp_abs,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": safe_divide(d_qp_abs, nrf_total),
        "d_gwp_rel": safe_divide(d_gwp_abs, nrf_total),
    }


# ============================================================
# B6.1b eigengenutzter Anteil erneuerbarer Energie
# ============================================================

def calculate_b6_1b_self_used_pv(pv_area, battery_storage, nrf_total):
    try:
        pv_area = float(str(pv_area).replace(",", "."))
    except (TypeError, ValueError):
        pv_area = 0

    if pv_area <= 0:
        return {
            "name": "B6.1b - eigengenutzter Anteil EE",
            "ac_qp_abs": 0,
            "ac_gwp_abs": 0,
            "d_qp_abs": 0,
            "d_gwp_abs": 0,
            "ac_qp_rel": 0,
            "ac_gwp_rel": 0,
            "d_qp_rel": 0,
            "d_gwp_rel": 0,
        }

    # Vereinfachter Ansatz:
    # ca. 180 kWh Stromertrag pro m² PV-Fläche und Jahr.
    # Ohne Speicher wird ein geringerer Eigenverbrauch angesetzt,
    # mit Speicher ein höherer Eigenverbrauch.
    pv_yield_kwh = pv_area * 180

    if battery_storage == "ja":
        self_use_factor = 0.75
    else:
        self_use_factor = 0.50

    self_used_kwh = pv_yield_kwh * self_use_factor

    grid_factor = ENERGY_FACTORS[
        "Nutzung - 1 kWh nationaler Netzstrommix"
    ]

    ac_qp_abs = -self_used_kwh * grid_factor["qp"]
    ac_gwp_abs = -self_used_kwh * grid_factor["gwp"]

    return {
        "name": "B6.1b - eigengenutzter Anteil EE",
        "ac_qp_abs": ac_qp_abs,
        "ac_gwp_abs": ac_gwp_abs,
        "d_qp_abs": 0,
        "d_gwp_abs": 0,
        "ac_qp_rel": safe_divide(ac_qp_abs, nrf_total),
        "ac_gwp_rel": safe_divide(ac_gwp_abs, nrf_total),
        "d_qp_rel": 0,
        "d_gwp_rel": 0,
    }


# ============================================================
# Gesamtergebnis
# ============================================================

def calculate_qng_result(
    nrf_total,
    nrf_tg,
    nrf_heated,
    an_geg,
    building_type,
    energy_standard,
    heating,
    ventilation,
    qng_level,
    pv_area,
    battery_storage,
):
    nrf_total = float(nrf_total)

    kg300 = calculate_kg300(
        building_type,
        nrf_total,
        float(nrf_tg),
    )

    kg400_sockel = calculate_kg400_sockel(
        energy_standard
    )

    kg400_gross = calculate_kg400_grossgeraete(
        heating,
        ventilation,
        nrf_total,
        float(nrf_tg),
    )

    b6_1a = calculate_b6_1a(
        ventilation,
        heating,
        an_geg,
        nrf_total,
    )

    user_electricity = calculate_user_electricity(
        nrf_total,
    )

    pv = calculate_pv(
        pv_area,
        battery_storage,
        nrf_total,
    )

    b6_1b = calculate_b6_1b_self_used_pv(
        pv_area,
        battery_storage,
        nrf_total,
    )

    parts = [
        kg300,
        kg400_sockel,
        kg400_gross,
        pv,
        b6_1a,
        user_electricity,
        b6_1b,
    ]

    total_ac_qp_rel = sum(
        part["ac_qp_rel"]
        for part in parts
    )

    total_ac_gwp_rel = sum(
        part["ac_gwp_rel"]
        for part in parts
    )

    total_d_qp_rel = sum(
        part["d_qp_rel"]
        for part in parts
    )

    total_d_gwp_rel = sum(
        part["d_gwp_rel"]
        for part in parts
    )

    qp_limit = QNG_LIMITS[qng_level]["qp"]
    gwp_limit = QNG_LIMITS[qng_level]["gwp"]

    qp_difference_percent = round(
        ((total_ac_qp_rel - qp_limit) / qp_limit) * 100,
        1
    )

    gwp_difference_percent = round(
        ((total_ac_gwp_rel - gwp_limit) / gwp_limit) * 100,
        1
    )
    qp_scale = max(total_ac_qp_rel, qp_limit)
    gwp_scale = max(total_ac_gwp_rel, gwp_limit)
    
    qp_limit_marker_percent = round((qp_limit / qp_scale) * 100, 1)
    gwp_limit_marker_percent = round((gwp_limit / gwp_scale) * 100, 1)
    
    if total_ac_qp_rel <= qp_limit:
        qp_green_percent = round((total_ac_qp_rel / qp_scale) * 100, 1)
        qp_red_percent = 0
    else:
        qp_green_percent = qp_limit_marker_percent
        qp_red_percent = round(100 - qp_limit_marker_percent, 1)
    
    if total_ac_gwp_rel <= gwp_limit:
        gwp_green_percent = round((total_ac_gwp_rel / gwp_scale) * 100, 1)
        gwp_red_percent = 0
    else:
        gwp_green_percent = gwp_limit_marker_percent
        gwp_red_percent = round(100 - gwp_limit_marker_percent, 1)

    return {
        "parts": parts,
        "total": {
            "ac_qp_rel": round(total_ac_qp_rel, 2),
            "ac_gwp_rel": round(total_ac_gwp_rel, 2),
            "d_qp_rel": round(total_d_qp_rel, 2),
            "d_gwp_rel": round(total_d_gwp_rel, 2),
            "qp_limit": qp_limit,
            "gwp_limit": gwp_limit,
            "qp_difference_percent": qp_difference_percent,
            "gwp_difference_percent": gwp_difference_percent,
            "qp_green_percent": qp_green_percent,
            "qp_red_percent": qp_red_percent,
            "qp_limit_marker_percent": qp_limit_marker_percent,
            "gwp_green_percent": gwp_green_percent,
            "gwp_red_percent": gwp_red_percent,
            "gwp_limit_marker_percent": gwp_limit_marker_percent,
            "qp_status": (
                "erfüllt"
                if total_ac_qp_rel <= qp_limit
                else "nicht erfüllt"
            ),
            "gwp_status": (
                "erfüllt"
                if total_ac_gwp_rel <= gwp_limit
                else "nicht erfüllt"
            ),
        },
    }
