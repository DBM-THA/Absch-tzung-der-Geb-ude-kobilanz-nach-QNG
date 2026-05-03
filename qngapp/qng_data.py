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
