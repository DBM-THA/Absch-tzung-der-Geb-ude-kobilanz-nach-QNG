# qngapp/qng_data.py

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


KG400_SOCKEL_VALUES = {
    "Effizienzhaus 55 oder schlechter": {
        "ac_qp_rel": 4.50,
        "ac_gwp_rel": 1.20,
        "d_qp_rel": -1.45,
        "d_gwp_rel": -0.52,
    },
    "Effizienzhaus 40": {
        "ac_qp_rel": 4.70,
        "ac_gwp_rel": 1.30,
        "d_qp_rel": -1.60,
        "d_gwp_rel": -0.61,
    },
}


KG400_GROSSGERAETE_VALUES = {
    "heating": {
        "Nahwärme, Pelletkessel": {
            "ac_qp_abs": 1785,
            "ac_gwp_abs": 570,
            "d_qp_abs": -148,
            "d_gwp_abs": -58,
        },
        "Fernwärme": {
            "ac_qp_abs": 1062,
            "ac_gwp_abs": 296,
            "d_qp_abs": -90,
            "d_gwp_abs": -32,
        },
        "Luft-Wasser-Wärmepumpe": {
            "ac_qp_abs": 1474,
            "ac_gwp_abs": 428,
            "d_qp_abs": -158,
            "d_gwp_abs": -53,
        },
        "Grundwasser-Wärmepumpe": {
            "ac_qp_abs": 924,
            "ac_gwp_abs": 254,
            "d_qp_abs": -79,
            "d_gwp_abs": -26,
        },
    },
    "ventilation": {
        "Zu-/Abluftanlage mit WRG": {
            "ac_qp_abs": 1220,
            "ac_gwp_abs": 317,
            "d_qp_abs": -153,
            "d_gwp_abs": -42,
        },
        "Abluftanlage ohne WRG": {
            "ac_qp_abs": 164,
            "ac_gwp_abs": 42,
            "d_qp_abs": -5,
            "d_gwp_abs": -2,
        },
    },
    "elevator": {
        "Fahrstuhl - Grundkomponenten": {
            "ac_qp_abs": 1960,
            "ac_gwp_abs": 629,
            "d_qp_abs": -222,
            "d_gwp_abs": -95,
        }
    },
}


QNG_LIMITS = {
    "QNG-PLUS": {
        "qp": 96,
        "gwp": 24,
    },
    "QNG-PREMIUM": {
        "qp": 64,
        "gwp": 20,
    },
}
# Endenergiebedarf je Kombination, bezogen auf AN_GEG = 6201 m² aus Excel
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


ENERGY_FACTORS = {
    "Nutzung - 1 kWh nationaler Netzstrommix": {
        "qp": 1.8616763889,
        "gwp": 0.53203,
    },
    "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK": {
        "qp": 0.0713205722,
        "gwp": 0.02533312,
    },
}


DEFAULT_ENERGY_CARRIERS = {
    "heating": "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK",
    "hot_water": "Nutzung - 1kWh Fernwärme aus Biomasse (fest) ohne KWK",
    "auxiliary": "Nutzung - 1 kWh nationaler Netzstrommix",
}


USER_ELECTRICITY_KWH_PER_M2 = 20
