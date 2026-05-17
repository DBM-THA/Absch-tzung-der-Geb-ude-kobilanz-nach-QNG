from django.test import TestCase

from qngapp.calculations import calculate_qng_result


class QNGCalculationTests(TestCase):

    def test_calculation_returns_qp_and_gwp(self):
        result = calculate_qng_result(
            nrf_total=1000,
            nrf_tg=0,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            qng_level="QNG-PLUS",
            an_geg=800,
            nrf_heated=800,
            pv_area=50,
            battery_storage="nein",
        )

        self.assertIn("total", result)
        self.assertIn("ac_qp_rel", result["total"])
        self.assertIn("ac_gwp_rel", result["total"])

    def test_result_contains_parts(self):
        result = calculate_qng_result(
            nrf_total=1000,
            nrf_tg=0,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            qng_level="QNG-PLUS",
        )

        self.assertIn("parts", result)
        self.assertGreater(len(result["parts"]), 0)

    def test_qng_status_exists(self):
        result = calculate_qng_result(
            nrf_total=1000,
            nrf_tg=0,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            qng_level="QNG-PLUS",
        )

        self.assertIn(result["total"]["qp_status"], ["erfüllt", "nicht erfüllt"])
        self.assertIn(result["total"]["gwp_status"], ["erfüllt", "nicht erfüllt"])
