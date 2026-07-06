# qngapp/qng_data.py

"""
Zentrale Datenbasis für das QNG-Webtool.

Diese Datei enthält feste Kennwerte, Grenzwerte und Faktoren,
die aus dem Excel-Tool abgeleitet wurden.

Wichtig:
- Hier stehen keine berechneten Endergebnisse.
- Hier stehen nur Kennwerte/Faktoren.
- Die eigentliche Berechnung passiert in calculations.py.
"""


# ============================================================
# QNG-Grenzwerte
# ============================================================

QNG_LIMITS_BY_BUILDING_CATEGORY = {
    "Mehrfamilienhaus": {
        "QNG-PLUS": {
            "qp": 96,
            "gwp": 24,
        },
        "QNG-PREMIUM": {
            "qp": 64,
            "gwp": 20,
        },
    },
    "Einfamilienhaus": {
        "QNG-PLUS": {
            "qp": 96,
            "gwp": 24,
        },
        "QNG-PREMIUM": {
            "qp": 64,
            "gwp": 20,
        },
    },
}

# Rückwärtskompatibilität:
# Wird weiterhin für Dropdowns und bestehende Views genutzt.
# Die eigentliche Berechnung verwendet QNG_LIMITS_BY_BUILDING_CATEGORY.
QNG_LIMITS = QNG_LIMITS_BY_BUILDING_CATEGORY["Mehrfamilienhaus"]


# ============================================================
# KG 300 - Bauwerk / Baukonstruktion
# Werte bezogen auf beheizte NRF
# Einheit:
# QP,ne: kWhPEne / m²NRF*a
# GWP: kg CO2-Äq. / m²NRF*a
# ============================================================

KG300_VALUES = {
    "Massivbauweise (KS + WDVS)": {
        "ac_qp_rel": 31.85,
        "ac_gwp_rel": 10.69,
        "d_qp_rel": -3.30,
        "d_gwp_rel": -0.87,
    },
    "Holzständer-AW": {
        "ac_qp_rel": 29.64,
        "ac_gwp_rel": 9.86,
        "d_qp_rel": -3.95,
        "d_gwp_rel": -1.05,
    },
    "Holzständer-AW und HBV-DE": {
        "ac_qp_rel": 29.60,
        "ac_gwp_rel": 9.41,
        "d_qp_rel": -8.76,
        "d_gwp_rel": -2.17,
    },
}


# Zusätzliche Kennwerte für Tiefgarage in KG300
# Im Excel wird die Tiefgarage separat berechnet:
# Wert = Kennwert * NRF_TG

KG300_TIEFGARAGE_VALUES = {
    "ac_qp_rel": 18.967,
    "ac_gwp_rel": 7.4946,
    "d_qp_rel": -0.8182,
    "d_gwp_rel": -0.2124,
}


# ============================================================
# KG 400 - Sockelbetrag
# Werte sind bereits relative Kennwerte pro m² NRF
# ============================================================

KG400_SOCKEL_VALUES = {
    "Effizienzhaus 55 oder schlechter": {
        "qp_ref_percent": "> 40",
        "ac_qp_rel": 4.50,
        "ac_gwp_rel": 1.20,
        "d_qp_rel": -1.45,
        "d_gwp_rel": -0.52,
    },
    "Effizienzhaus 40": {
        "qp_ref_percent": "<= 40",
        "ac_qp_rel": 4.70,
        "ac_gwp_rel": 1.30,
        "d_qp_rel": -1.60,
        "d_gwp_rel": -0.61,
    },
}


# ============================================================
# KG 400 - Großgeräte
# Werte bezogen auf beheizte NRF
# Einheit:
# QP,ne: kWhPEne / m²NRF*a
# GWP: kg CO2-Äq. / m²NRF*a
# ============================================================

KG400_GROSSGERAETE_VALUES = {
    "heating": {
        "Nahwärme, Pelletkessel": {
            "ac_qp_rel": 0.338,
            "ac_gwp_rel": 0.108,
            "d_qp_rel": -0.028,
            "d_gwp_rel": -0.011,
        },
        "Fernwärme": {
            "ac_qp_rel": 0.201,
            "ac_gwp_rel": 0.056,
            "d_qp_rel": -0.017,
            "d_gwp_rel": -0.006,
        },
        "Luft-Wasser-Wärmepumpe": {
            "ac_qp_rel": 0.279,
            "ac_gwp_rel": 0.081,
            "d_qp_rel": -0.030,
            "d_gwp_rel": -0.010,
        },
        "Grundwasser-Wärmepumpe": {
            "ac_qp_rel": 0.175,
            "ac_gwp_rel": 0.048,
            "d_qp_rel": -0.015,
            "d_gwp_rel": -0.005,
        },
    },
    "ventilation": {
        "Zu-/Abluftanlage mit WRG": {
            "ac_qp_rel": 0.231,
            "ac_gwp_rel": 0.060,
            "d_qp_rel": -0.029,
            "d_gwp_rel": -0.008,
        },
        "Abluftanlage ohne WRG": {
            "ac_qp_rel": 0.031,
            "ac_gwp_rel": 0.008,
            "d_qp_rel": -0.001,
            "d_gwp_rel": -0.0004,
        },
    },
    "elevator": {
        "Fahrstuhl - Grundkomponenten": {
            "ac_qp_rel": 0.371,
            "ac_gwp_rel": 0.119,
            "d_qp_rel": -0.042,
            "d_gwp_rel": -0.018,
        }
    },
}


# ============================================================
# Modul B6.1a - Energiebedarf
# Endenergiebedarf je Kombination aus Lüftung + Heizung
#
# Basis aus Excel:
# bezogen auf AN_GEG = 6201 m²
#
# Einheit:
# heating / hot_water / auxiliary = kWh/a
# ============================================================

END_ENERGY_BASE_AN_GEG = 6201

END_ENERGY_DEMANDS = {
    ("Zu-/Abluftanlage mit WRG", "Nahwärme, Pelletkessel"): {
        "heating": 26749,
        "hot_water": 177635,
        "auxiliary": 10862,
    },
    ("Zu-/Abluftanlage mit WRG", "Fernwärme"): {
        "heating": 21775,
        "hot_water": 177635,
        "auxiliary": 10963,
    },
    ("Zu-/Abluftanlage mit WRG", "Luft-Wasser-Wärmepumpe"): {
        "heating": 7818,
        "hot_water": 64491,
        "auxiliary": 12968,
    },
    ("Zu-/Abluftanlage mit WRG", "Grundwasser-Wärmepumpe"): {
        "heating": 3687,
        "hot_water": 54884,
        "auxiliary": 11302,
    },
    ("Abluftanlage ohne WRG", "Nahwärme, Pelletkessel"): {
        "heating": 106509,
        "hot_water": 177611,
        "auxiliary": 4619,
    },
    ("Abluftanlage ohne WRG", "Fernwärme"): {
        "heating": 105786,
        "hot_water": 177611,
        "auxiliary": 4542,
    },
    ("Abluftanlage ohne WRG", "Luft-Wasser-Wärmepumpe"): {
        "heating": 37843,
        "hot_water": 64481,
        "auxiliary": 4361,
    },
    ("Abluftanlage ohne WRG", "Grundwasser-Wärmepumpe"): {
        "heating": 17186,
        "hot_water": 54877,
        "auxiliary": 4428,
    },
}


# ============================================================
# Endenergieträger / Energiefaktoren
#
# qp:
# Excel-Faktor PENRT in kWhPEne/kWh Endenergie
#
# gwp:
# kg CO2-Äq. / kWh Endenergie
# ============================================================

ENERGY_FACTORS = {
    "Nutzung - 1 kWh Endenergie aus Gas Brennwert (entspr. EnEV)": {
        "qp": 1.0904417083,
        "gwp": 0.23480494,
        "gwp_d2": 0,
    },
    "Nutzung - 1 kWh Endenergie aus Gas Niedertemperatur (entspr. EnEV)": {
        "qp": 1.0904417083,
        "gwp": 0.23386801,
        "gwp_d2": 0,
    },
    "Nutzung - 1 kWh Endenergie aus Hackschnitzeln (entspr. EnEV)": {
        "qp": 0.0183984889,
        "gwp": 0.0076469,
        "gwp_d2": 0,
    },
    "Nutzung - 1 kWh Endenergie aus Holzpellets (entspr. EnEV)": {
        "qp": 0.0756241389,
        "gwp": 0.02108244,
        "gwp_d2": 0,
    },
    "Nutzung - 1 kWh Endenergie aus Öl Niedertemperatur und Brennwert (entspr. EnEV)": {
        "qp": 1.1643196333,
        "gwp": 0.29956767,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Biogas mit KWK": {
        "qp": 0.0759616972,
        "gwp": 0.05629219,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Biomasse (fest) mit KWK": {
        "qp": 0.0324461361,
        "gwp": 0.0115258798,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Braunkohle mit KWK": {
        "qp": 0.7544026944,
        "gwp": 0.3062231,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Erdgas mit KWK": {
        "qp": 0.6823214167,
        "gwp": 0.14776562,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Heizöl (leicht) mit KWK": {
        "qp": 0.6998328528,
        "gwp": 0.1888197,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Steinkohle mit KWK": {
        "qp": 0.8031568611,
        "gwp": 0.284130227,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Biogas ohne KWK": {
        "qp": 0.2369037194,
        "gwp": 0.17557317,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK": {
        "qp": 0.0713205722,
        "gwp": 0.02533312,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Braunkohle ohne KWK": {
        "qp": 1.3067893972,
        "gwp": 0.53044599,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Erdgas ohne KWK": {
        "qp": 1.3430654278,
        "gwp": 0.2908654,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Heizöl (leicht) ohne KWK": {
        "qp": 1.5466306056,
        "gwp": 0.41729154,
        "gwp_d2": 0,
    },
    "Nutzung - 1kWh Fernwärme aus Steinkohle ohne KWK": {
        "qp": 1.5468266889,
        "gwp": 0.54720278,
        "gwp_d2": 0,
    },
    "Nutzung - 1 kWh nationaler Netzstrommix": {
        "qp": 1.8616763889,
        "gwp": 0.53203,
        "gwp_d2": 0,
    },
}


# Aktuell im Webtool verwendete Standard-Energieträger.
# Diese Struktur kann später über die GUI/Admin-Oberfläche erweitert werden.

DEFAULT_ENERGY_CARRIERS = {
    "heating": "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK",
    "hot_water": "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK",
    "auxiliary": "Nutzung - 1 kWh nationaler Netzstrommix",
}


# ============================================================
# Nutzerstrom B6.3
# ============================================================

USER_ELECTRICITY_KWH_PER_M2 = 20


# ============================================================
# Photovoltaik
#
# Parameter aus den Excel-Formeln.
# Die aktuelle calculations.py kann diese Werte später direkt nutzen.
# Im Moment dienen sie zusätzlich der Dokumentation der festen PV-Werte.
# ============================================================

PV_FORMULA_PARAMS = {
    "pv_parts": {
        "lt_300": {
            "ac_qp": {
                "a": 12600,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
            "ac_gwp": {
                "a": 3515,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
            "d_qp": {
                "a": -2.0931,
                "formula": "a * pv_area",
            },
            "d_gwp": {
                "a": -0.6792,
                "formula": "a * pv_area",
            },
        },
        "gte_300_without_battery": {
            "ac_qp": {
                "a": 12600,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
            "ac_gwp": {
                "a": 3515,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
            "d_qp": {
                "a": -635,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
            "d_gwp": {
                "a": -206,
                "b": 0.0061,
                "formula": "a * (1 - exp(-b * pv_area))",
            },
        },
        "gte_300_with_battery": {
            "ac_qp": {
                "a": 41125,
                "b": 0.0023,
                "offset": 89.72,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
            "ac_gwp": {
                "a": 11425,
                "b": 0.0023,
                "offset": 89.11,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
            "d_qp": {
                "a": -2027,
                "b": 0.0022,
                "offset": 72.7,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
            "d_gwp": {
                "a": -639,
                "b": 0.0022,
                "offset": 72.21,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
        },
    },
    "b6_1b": {
        "lt_300": {
            "qp": {
                "a": -222.58,
                "formula": "a * pv_area",
            },
            "gwp": {
                "a": -63.608,
                "formula": "a * pv_area",
            },
        },
        "gte_300_without_battery": {
            "qp": {
                "base": -70065,
                "a": 3172.11,
                "b": -0.011,
                "offset": 303.36,
                "formula": "base + a * exp(b * (pv_area - offset))",
            },
            "gwp": {
                "base": -20025,
                "a": 842.39,
                "b": -0.0108,
                "offset": 310.42,
                "formula": "base + a * exp(b * (pv_area - offset))",
            },
        },
        "gte_300_with_battery": {
            "qp": {
                "a": -184610,
                "b": 0.0022,
                "offset": 61.27,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
            "gwp": {
                "a": -52760,
                "b": 0.0022,
                "offset": 61.26,
                "formula": "a * (1 - exp(-b * (pv_area - offset)))",
            },
        },
    },
    "d2": {
        "gte_300_without_battery": {
            "qp": {
                "a": -87.72,
                "b": 24860,
                "formula": "a * pv_area + b",
            },
            "gwp": {
                "a": -60.781,
                "b": 16841,
                "formula": "a * pv_area + b",
            },
        },
        "gte_350_with_battery": {
            "qp": {
                "a": -0.0202,
                "b": -20.884,
                "c": 9533.1,
                "formula": "a * pv_area**2 + b * pv_area + c",
            },
            "gwp": {
                "a": -0.0137,
                "b": -14.148,
                "c": 6458.2,
                "formula": "a * pv_area**2 + b * pv_area + c",
            },
        },
    },
}


# ============================================================
# Referenzfall aus dem Excel-Tool
#
# Wird nur für Validierung/Tests genutzt.
# ============================================================

EXCEL_REFERENCE_CASE = {
    "project_name": "Masterarbeit",
    "qng_level": "QNG-PLUS",
    "bgf": 6616,
    "an_geg": 6201,
    "nrf_total": 5282,
    "nrf_heated": 5282,
    "nrf_tg": 0,
    "energy_standard": "Effizienzhaus 40",
    "building_type": "Massivbauweise (KS + WDVS)",
    "ventilation": "Zu-/Abluftanlage mit WRG",
    "heating": "Nahwärme, Pelletkessel",
    "pv_area": 300,
    "battery_storage": "nein",
    "expected": {
        "ac_qp_rel": 70.6727225069,
        "ac_gwp_rel": 21.9379464187,
        "d_qp_rel": -5.3755879183,
        "d_gwp_rel": -1.8135268468,
    },
}
