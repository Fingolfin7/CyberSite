from django.db import models
from django.utils import timezone
from PIL import Image


assessments = [
    ("White Box:", "White Box"),
    ("Grey Box:", "Grey Box"),
    ("Black Box:", "Black Box")
]

recon_tools = [
    ("", "Select Tool"),
    ("Nmap", "Nmap"),
    ("Nessus", "Nessus"),
    ("Shodan", "Shodan"),
    ("OpenVAS", "OpenVAS"),
    ("Metasploit", "Metasploit"),
    ("Nikto", "Nikto"),
    ("Other", "Other"),
]

severity_levels = [
    ("", "Severity"),
    ("Critical", "Critical"),
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
    ("Info", "Info"),
 ]


class Cases(models.Model):
    caseName = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    caseLead = models.CharField(max_length=100)
    orgHandler = models.CharField(max_length=100)
    assessmentType = models.CharField(max_length=100, choices=assessments,
                                      blank=False, default='Unspecified')
    scope = models.TextField()
    logo = models.ImageField(upload_to=f'Cases/{caseName}/Logos')
    createDate = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.caseName}"

    def save(self):
        super().save()
        img = Image.open(self.logo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.logo.path)

    class Meta:
        verbose_name_plural = "Cases"


class Recon(models.Model):
    case = models.OneToOneField(Cases, on_delete=models.CASCADE)
    tools = models.TextField()
    passive_sources = models.TextField()

    def __str__(self):
        return f"{self.case.caseName} Recon"

    class Meta:
        verbose_name_plural = "Recon"


class Issues(models.Model):
    case = models.ForeignKey(Cases, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    severity = models.CharField(blank=True, max_length=100, choices=severity_levels)
    affected_hosts = models.TextField(blank=True)
    description = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    reference = models.TextField(blank=True)
    cvss_rating = models.FloatField(blank=True, null=True)
    proof_screenshot = models.ImageField(blank=True, upload_to=f'Cases/Screenshots')

    def __str__(self):
        return f"{self.case.caseName} Issue ({self.id})"

    class Meta:
        verbose_name_plural = "Issues"

