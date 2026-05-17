from django.test import TestCase

from qngapp.calculations import calculate_qng_result


DEFAULT_INPUTS = {
    "nrf_total": 1000,
    "nrf_tg": 0,
    "nrf_heated": 1000,
    "an_geg": 1000,
    "building_type": "Massivbauweise (KS + WDVS)",
    "energy_standard": "Effizienzhaus 40",
    "heating": "Luft-Wasser-Wärmepumpe",
    "ventilation": "Zu-/Abluftanlage mit WRG",
    "qng_level": "QNG-PLUS",
    "pv_area": 50,
    "battery_storage": "nein",
}


class QNGCalculationTests(TestCase):

    def test_calculation_returns_qp_and_gwp(self):
        result = calculate_qng_result(**DEFAULT_INPUTS)

        self.assertIn("total", result)
        self.assertIn("ac_qp_rel", result["total"])
        self.assertIn("ac_gwp_rel", result["total"])

    def test_result_contains_parts(self):
        result = calculate_qng_result(**DEFAULT_INPUTS)

        self.assertIn("parts", result)
        self.assertGreater(len(result["parts"]), 0)

    def test_qng_status_exists(self):
        result = calculate_qng_result(**DEFAULT_INPUTS)

        self.assertIn(result["total"]["qp_status"], ["erfüllt", "nicht erfüllt"])
        self.assertIn(result["total"]["gwp_status"], ["erfüllt", "nicht erfüllt"])

    def test_pv_reduces_gwp(self):
        without_pv = calculate_qng_result(
            **{
                **DEFAULT_INPUTS,
                "pv_area": 0,
            }
        )

        with_pv = calculate_qng_result(
            **{
                **DEFAULT_INPUTS,
                "pv_area": 300,
            }
        )

        self.assertLess(
            with_pv["total"]["ac_gwp_rel"],
            without_pv["total"]["ac_gwp_rel"],
        )

    def test_premium_limits_are_stricter_than_plus(self):
        plus = calculate_qng_result(
            **{
                **DEFAULT_INPUTS,
                "qng_level": "QNG-PLUS",
            }
        )

        premium = calculate_qng_result(
            **{
                **DEFAULT_INPUTS,
                "qng_level": "QNG-PREMIUM",
            }
        )

        self.assertLess(premium["total"]["qp_limit"], plus["total"]["qp_limit"])
        self.assertLess(premium["total"]["gwp_limit"], plus["total"]["gwp_limit"])

    def test_tiefgarage_changes_result(self):
        without_tg = calculate_qng_result(**DEFAULT_INPUTS)

        with_tg = calculate_qng_result(
            **{
                **DEFAULT_INPUTS,
                "nrf_total": 1200,
                "nrf_tg": 200,
                "nrf_heated": 1000,
            }
        )

        self.assertNotEqual(
            without_tg["parts"][0]["ac_qp_rel"],
            with_tg["parts"][0]["ac_qp_rel"],
        )
