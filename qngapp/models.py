from django.db import models


class Building(models.Model):
    project_name = models.CharField(max_length=200, default="Beispielgebäude")
    nrf_total = models.FloatField(default=0)
    nrf_tg = models.FloatField(default=0)
    nrf_heated = models.FloatField(default=0)
    an_geg = models.FloatField(default=0)
    building_type = models.CharField(max_length=200)
    energy_standard = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name


class Scenario(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name="scenarios"
    )

    heating = models.CharField(max_length=200)
    ventilation = models.CharField(max_length=200)
    pv_area = models.FloatField(default=0)
    battery_storage = models.CharField(max_length=20, default="nein")
    qng_level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.building.project_name} – {self.qng_level}"


class Result(models.Model):
    scenario = models.OneToOneField(
        Scenario,
        on_delete=models.CASCADE,
        related_name="result"
    )

    ac_qp_rel = models.FloatField(default=0)
    ac_gwp_rel = models.FloatField(default=0)
    qp_limit = models.FloatField(default=0)
    gwp_limit = models.FloatField(default=0)
    qp_status = models.CharField(max_length=50)
    gwp_status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ergebnis: {self.scenario}"
