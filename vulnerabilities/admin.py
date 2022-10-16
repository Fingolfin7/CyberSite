from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(VulnerabilitiesGeneral)
admin.site.register(VulnerabilitiesCWE)
admin.site.register(VulnerabilitiesEnterprise)
admin.site.register(VulnerabilitiesMobile)
admin.site.register(VulnerabilitiesOWASP)
admin.site.register(VulnerabilitiesImported)
