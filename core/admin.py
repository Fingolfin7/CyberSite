from django.contrib import admin
from .models import Cases, Recon, Issues, PoC

admin.site.register(Cases)
admin.site.register(Recon)
admin.site.register(Issues)
admin.site.register(PoC)
