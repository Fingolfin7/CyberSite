from django.db import models
from core.models import severity_levels


class VulnerabilitiesGeneral(models.Model):
    title = models.CharField(primary_key=True, max_length=500)
    description = models.TextField(blank=True)
    severity = models.CharField(blank=True, max_length=100, choices=severity_levels)
    reference = models.TextField(blank=True)
    cvss_rating = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "General"

    def __str__(self):
        return f"{self.title}"


class VulnerabilitiesCWE(VulnerabilitiesGeneral):
    class Meta:
        verbose_name_plural = "CWE"


class VulnerabilitiesEnterprise(VulnerabilitiesGeneral):
    class Meta:
        verbose_name_plural = "Enterprise"


class VulnerabilitiesMobile(VulnerabilitiesGeneral):
    class Meta:
        verbose_name_plural = "Mobile"


class VulnerabilitiesOWASP(VulnerabilitiesGeneral):
    class Meta:
        verbose_name_plural = "OWASP"


class VulnerabilitiesImported(VulnerabilitiesGeneral):
    class Meta:
        verbose_name_plural = "Imported"
