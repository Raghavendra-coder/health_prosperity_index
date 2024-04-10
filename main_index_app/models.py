from django.db import models
import uuid


class TimeStampModel(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class YearModel(models.Model):
    id_year = models.IntegerField()
    year = models.CharField(max_length=4, null=True)

    class Meta:
        abstract = True


class GeographyModel(models.Model):
    geography = models.CharField(max_length=30, null=True)
    id_geography = models.CharField(max_length=30, null=True)
    slug_geography = models.CharField(max_length=30, null=True)

    class Meta:
        abstract = True


GENDER = (
        ('Male', "Male"),
        ('Female', "Female"),
    )

ID_GENDER = (
        (1, 1),
        (2, 2),
    )

ID_HEALTH_COVERAGE = (
    (0, 0),
    (1, 1),
)

HEALTH_COVERAGE = (
    ("Public", "Public"),
    ("Private", "Private"),
)


class EmploymentData(YearModel, GeographyModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_gender = models.IntegerField(choices=ID_GENDER)
    gender = models.CharField(max_length=6, choices=GENDER, null=True)
    id_age = models.IntegerField()
    age = models.CharField(max_length=3, null=True)
    id_workforce_status = models.BooleanField()
    workforce_status = models.CharField(max_length=5, null=True)
    total_population = models.BigIntegerField()


class WorkingPopulationData(YearModel, GeographyModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_age = models.IntegerField()
    age = models.CharField(max_length=3, null=True)
    id_gender = models.IntegerField(choices=ID_GENDER)
    gender = models.CharField(max_length=6, choices=GENDER, null=True)
    total_population = models.BigIntegerField()
    total_population_moe_appx = models.FloatField()
    average_wage = models.FloatField(null=True)
    average_wage_moe_appx = models.FloatField(null=True)


class HousingData(YearModel, GeographyModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_real_estate_taxes_paid = models.FloatField()
    real_estate_taxes_paid = models.CharField(max_length=30, null=True)
    real_estate_taxes_by_mortgage = models.FloatField()
    real_estate_taxes_by_mortgage_moe = models.FloatField()


class EquityData(YearModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_race = models.IntegerField()
    race = models.CharField(max_length=20, null=True)
    id_state = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=30, null=True)
    slug_state = models.CharField(max_length=30, null=True)
    household_income_by_race = models.FloatField(null=True)
    household_income_by_race_moe = models.FloatField(null=True)


class HealthCareData(YearModel, GeographyModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_gender = models.IntegerField(choices=ID_GENDER)
    gender = models.CharField(max_length=6, choices=GENDER, null=True)
    id_health_coverage = models.IntegerField(choices=ID_HEALTH_COVERAGE)
    health_coverage = models.CharField(max_length=7, choices=HEALTH_COVERAGE)
    health_insurance_by_gender_and_age = models.BigIntegerField(null=True)


class PovertyData(YearModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_state = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=30, null=True)
    slug_state = models.CharField(max_length=30, null=True)
    severe_housing_problems = models.FloatField(null=True)
    severe_housing_problems_ci_high = models.FloatField(null=True)
    severe_housing_problems_ci_low = models.FloatField(null=True)


class ChildMortalityRate(YearModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    id_state = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=30, null=True)
    slug_state = models.CharField(max_length=30, null=True)
    child_mortality = models.FloatField(null=True)
    child_mortality_ci_high = models.FloatField(null=True)
    child_mortality_ci_low = models.FloatField(null=True)


class HealthProsperityIndexData(YearModel, TimeStampModel):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    employment_total_population = models.IntegerField(null=True, blank=True)
    working_total_population = models.IntegerField(null=True, blank=True)
    real_estate_taxes_by_mortgage = models.FloatField(null=True, blank=True)
    household_income = models.FloatField(null=True, blank=True)
    severe_housing_problem = models.FloatField(null=True, blank=True)
    child_mortality_rate = models.FloatField(null=True, blank=True)
    working_average_wage = models.FloatField(null=True, blank=True)
    health_care_insurance = models.FloatField(null=True, blank=True)