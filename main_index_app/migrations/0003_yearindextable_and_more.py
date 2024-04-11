# Generated by Django 4.2.11 on 2024-04-11 10:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_index_app', '0002_rename_average_wage_moe_appx_workingpopulationdata_average_wage_appx_moe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearIndexTable',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.CharField(max_length=4)),
                ('health_prosperity_index', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='child_mortality_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='employment_total_population',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='health_care_insurance',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='household_income',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='real_estate_taxes_by_mortgage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='severe_housing_problem',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='working_average_wage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='healthprosperityindexdata',
            name='working_total_population',
            field=models.IntegerField(null=True),
        ),
    ]