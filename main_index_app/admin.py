from django.contrib import admin
from .models import *


class HealthProsperityIndexDataAdmin(admin.ModelAdmin):
    list_display = ("year", "employment_total_population", "working_total_population", "real_estate_taxes_by_mortgage",
                    "household_income", "severe_housing_problem", "child_mortality_rate", "working_average_wage",
                    "health_care_insurance")
# Register your models here.
admin.site.register(EmploymentData)
admin.site.register(WorkingPopulationData)
admin.site.register(HousingData)
admin.site.register(EquityData)
admin.site.register(HealthCareData)
admin.site.register(PovertyData)
admin.site.register(ChildMortalityRate)
admin.site.register(HealthProsperityIndexData, HealthProsperityIndexDataAdmin)
admin.site.register(YearIndexTable)