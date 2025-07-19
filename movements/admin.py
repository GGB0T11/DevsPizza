from django.contrib import admin

from .models import Inflow, Outflow

admin.site.register(Outflow)
admin.site.register(Inflow)
