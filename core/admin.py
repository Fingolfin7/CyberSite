from django.contrib import admin
from .models import *

admin.site.register(Cases)
admin.site.register(Recon)
admin.site.register(Issues)
admin.site.register(PoC)


admin.site.site_header = 'Bakertilly Cyber'
admin.site.site_title = 'Bakertilly Cyber'
admin.site.index_title = 'Admin'
