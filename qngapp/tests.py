from django.test import TestCase
from django.urls import reverse

from qngapp.calculations import calculate_qng_result
from qngapp.models import Building, Scenario, Result


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

    def test_pv_changes_gwp(self):
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

        self.assertNotEqual(
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

    def test_tiefgarage_changes_kg300_absolute_result(self):
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
            without_tg["parts"][0]["ac_qp_abs"],
            with_tg["parts"][0]["ac_qp_abs"],
        )

    def test_empty_pv_area_is_handled(self):
    result = calculate_qng_result(
        **{
            **DEFAULT_INPUTS,
            "pv_area": "",
        }
    )

    self.assertIn("total", result)


class QNGDatabaseTests(TestCase):

    def test_building_can_be_created(self):
        building = Building.objects.create(
            project_name="Testgebäude",
            nrf_total=1000,
            nrf_tg=0,
            nrf_heated=1000,
            an_geg=1200,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
        )

        self.assertEqual(Building.objects.count(), 1)
        self.assertEqual(str(building), "Testgebäude")

    def test_scenario_and_result_can_be_created(self):
        building = Building.objects.create(
            project_name="Testgebäude",
            nrf_total=1000,
            nrf_tg=0,
            nrf_heated=1000,
            an_geg=1200,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
        )

        scenario = Scenario.objects.create(
            building=building,
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            pv_area=300,
            battery_storage="ja",
            qng_level="QNG-PLUS",
        )

        result = Result.objects.create(
            scenario=scenario,
            ac_qp_rel=65.5,
            ac_gwp_rel=20.5,
            qp_limit=96,
            gwp_limit=24,
            qp_status="erfüllt",
            gwp_status="erfüllt",
        )

        self.assertEqual(building.scenarios.count(), 1)
        self.assertEqual(scenario.result, result)
        self.assertEqual(result.qp_status, "erfüllt")

    def test_deleting_building_deletes_scenarios_and_results(self):
        building = Building.objects.create(
            project_name="Testgebäude",
            nrf_total=1000,
            nrf_tg=0,
            nrf_heated=1000,
            an_geg=1200,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
        )

        scenario = Scenario.objects.create(
            building=building,
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            pv_area=300,
            battery_storage="ja",
            qng_level="QNG-PLUS",
        )

        Result.objects.create(
            scenario=scenario,
            ac_qp_rel=65.5,
            ac_gwp_rel=20.5,
            qp_limit=96,
            gwp_limit=24,
            qp_status="erfüllt",
            gwp_status="erfüllt",
        )

        building.delete()

        self.assertEqual(Building.objects.count(), 0)
        self.assertEqual(Scenario.objects.count(), 0)
        self.assertEqual(Result.objects.count(), 0)


class QNGWorkflowTests(TestCase):

    def setUp(self):
        self.building = Building.objects.create(
            project_name="Workflow-Testgebäude",
            nrf_total=1000,
            nrf_tg=0,
            nrf_heated=1000,
            an_geg=1200,
            building_type="Massivbauweise (KS + WDVS)",
            energy_standard="Effizienzhaus 40",
        )

        self.scenario = Scenario.objects.create(
            building=self.building,
            heating="Luft-Wasser-Wärmepumpe",
            ventilation="Zu-/Abluftanlage mit WRG",
            pv_area=300,
            battery_storage="ja",
            qng_level="QNG-PLUS",
        )

        self.result = Result.objects.create(
            scenario=self.scenario,
            ac_qp_rel=65.5,
            ac_gwp_rel=20.5,
            qp_limit=96,
            gwp_limit=24,
            qp_status="erfüllt",
            gwp_status="erfüllt",
        )

    def test_project_list_view_loads(self):
        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Workflow-Testgebäude")

    def test_project_detail_view_loads(self):
        response = self.client.get(
            reverse("project_detail", args=[self.building.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gespeicherte Szenarien")
        self.assertContains(response, "Luft-Wasser-Wärmepumpe")

    def test_compare_scenarios_requires_at_least_two_scenarios(self):
        response = self.client.get(
            reverse("compare_scenarios", args=[self.building.id]),
            {"scenario_ids": [self.scenario.id]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitte mindestens zwei Szenarien auswählen.")

    def test_deleted_project_detail_redirects_to_building(self):
        deleted_id = self.building.id
        self.building.delete()

        response = self.client.get(
            reverse("project_detail", args=[deleted_id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("building"))

    def test_delete_scenario_view_deletes_scenario(self):
        response = self.client.post(
            reverse("delete_scenario", args=[self.scenario.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Scenario.objects.count(), 0)
        self.assertEqual(Result.objects.count(), 0)

    def test_delete_project_view_deletes_project(self):
        response = self.client.post(
            reverse("delete_project", args=[self.building.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Building.objects.count(), 0)
        self.assertEqual(Scenario.objects.count(), 0)
        self.assertEqual(Result.objects.count(), 0)
