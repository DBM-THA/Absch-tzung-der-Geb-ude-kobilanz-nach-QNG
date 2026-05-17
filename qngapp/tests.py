from django.test import TestCase
from qngapp.calculations import calculate_result


class QNGCalculationTests(TestCase):

    def setUp(self):
        self.building = {
            "project_name": "Testgebäude",
            "nrf_total": 1000,
            "nrf_heated": 800,
            "building_type": "Massivbauweise (KS + WDVS)",
            "energy_standard": "GEG"
        }

        self.scenario = {
            "heating": "Wärmepumpe",
            "ventilation": "Lüftungsanlage mit WRG",
            "pv_area": 50,
            "battery_storage": "nein",
            "qng_level": "QNG-PLUS"
        }

    def test_calculation_returns_result(self):
        result = calculate_result(
            self.building,
            self.scenario
        )

        self.assertIn("total", result)

    def test_result_contains_qp_and_gwp(self):
        result = calculate_result(
            self.building,
            self.scenario
        )

        self.assertIn("ac_qp_rel", result["total"])
        self.assertIn("ac_gwp_rel", result["total"])

    def test_result_contains_parts(self):
        result = calculate_result(
            self.building,
            self.scenario
        )

        self.assertIn("parts", result)
        self.assertGreater(len(result["parts"]), 0)
