from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Policy(models.Model):
    class Meta:
        verbose_name = 'Policy'
        verbose_name_plural = 'Policies'

    class Type(models.TextChoices):
        HOME = "HOME", _("Home")
        AUTO = "AUTO", _("Auto")
        HEALTH = "HEALTH", _("Health")
        TRAVEL = "TRAVEL", _("Travel")
        LIFE = "LIFE", _("Life")

    policy_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, blank=False, null=False)
    policy_type = models.CharField(max_length=20, choices=Type, null=False)
    expiry_date = models.DateField(null=False, validators=[MinValueValidator(limit_value=timezone.localdate())])

    @admin.display(
        boolean=True,
        ordering="expiry_date",
        description="Is expired?",
    )
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    def __str__(self):
        return f"{self.policy_id} - {self.customer_name} - ${self.policy_type}"
