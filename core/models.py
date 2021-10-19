from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# Create your models here.
class Unit(models.Model):
    """Contains sherif's every unit data

    Args:
        user ([model User]): [authenticated registered user]
        log ([datetime timestamp]): [tencode logs],
        name ([string]): [name of the unit],
        shift ([string]): [shift of the unit - day/night],
        tencode ([string]): [tencode title - ENRT, ARRVD, AJAIL, CMPLT]
        tencode_complete_time ([string]): [tencode completion time in seconds]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128, null=True, blank=True)
    log = models.DateTimeField(default=timezone.now)
    shift = models.CharField(max_length=128, null=True, blank=True)
    tencode = models.CharField(max_length=256, null=True, blank=True)
    tencode_complete_time = models.CharField(
        max_length=256, null=True, blank=True)

    def __str__(self):
        return f'{self.name} | {self.shift}'


class JailPopulation(models.Model):
    """Contains jail population per date

    Args:
        user ([model User]): [authenticated registered user]
        date ([datetime]): [date]
        count_population ([model IntegerField]): [total jail population on a date]
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(null=True, blank=True)
    count_population = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.date | self.count_population


class SupplyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    supplier_name = models.CharField(max_length=128, null=True, blank=True)
    paid_year = models.CharField(max_length=128, null=True, blank=True)
    total_net_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    bin = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self) -> str:
        return self.supplier_name
