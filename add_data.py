import os
import json
import time
from pathlib import Path
import pandas as pd
import numpy as np
import requests
import streamlit as st
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from django.apps import apps
from django.utils.text import slugify
from main_index_app.models import *
from progress import progress_bar


BASE_DIR = Path(__file__).resolve().parent

json_file_path = BASE_DIR / 'datausa_endpoints.json'


def insert_data(data, model_name):
    """
    This function is used to add data from datausa to our relative database model
    :param data:
    :param model_name:
    :return:
    """
    ModelName = apps.get_model(app_label='main_index_app', model_name=model_name)
    for row in data:
        insert_row = dict()
        for key, value in row.items():
            slugified_key = slugify(key).replace("-", "_")
            if hasattr(ModelName, slugified_key):
                insert_row[slugified_key] = value
        instance = ModelName(**insert_row)
        instance.save()
        st.write(ModelName.objects.all().values('id')[0])


def extract_api_data(endpoint):
    """
    This function is used to get data from datausa endpoints
    :param endpoint:
    :return:
    """
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()['data']
    else:
        data = []

    return data


def insert_data_index_table(field_name, data: dict = dict()):
    """
    This function insert data in HealthProsperityIndexData model
    field_name: field that need to be updated
    data: dictionary objects with years as keys i.e. {'2014': 136275667, '2015': 138563308, '2016': 140806612
    """
    for key, value in data.items():
        if not value:
            value = 0
        if isinstance(value, float):
            value = round(value, 4)
        instance = HealthProsperityIndexData.objects.filter(year=key).first()
        if instance:
            setattr(instance, field_name, value)
        else:
            instance = HealthProsperityIndexData(**{"year": key, field_name: value})

        instance.save()


def update_data_in_column(model_name, deciding_field, health_index_field_name, operation="sum"):
    """
    This function prepare data to update the DB.
    model_name: Model that needs to be updated
    deciding_field: Field that need to calculate health index
    health_index_field_name: equivalent field name in HealthProsperityIndexData model to store column data
    operation: what resulted output is required from column i.e. sum, mean. default is sum
    """

    ModelName = apps.get_model(app_label='main_index_app', model_name=model_name)
    j = ModelName.objects.all().only('year', deciding_field).values('year', deciding_field)
    df = pd.DataFrame.from_records(j)
    grouped_year_df = df.groupby("year")[deciding_field].agg([operation]).rename(
        columns={operation: deciding_field}
    )
    grouped_year_df.fillna(0, inplace=True)
    return_dict = grouped_year_df.to_dict()[deciding_field]
    insert_data_index_table(health_index_field_name, return_dict)


def populate_data(add=False):
    """
        Populate/save the data from datausa to all tables in database
    """

    try:
        with open(json_file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    else:
        progress_count = 0
        db_count = 1
        for value in data.values():
            endpoint = value['endpoint']
            model_name = value['model_name']
            if add:
                progress_text = f"Updating db {db_count} out of 9"
                progress_bar.progress(progress_count, text=progress_text)
            data = extract_api_data(endpoint)
            if len(data):
                insert_data(data, model_name)
            progress_count += 11
            db_count += 1


def populate_health_index_table():
    """
    Populate the data in HealthProsperityIndexData table
    """
    update_data_in_column('EmploymentData', 'total_population', 'employment_total_population')
    update_data_in_column('WorkingPopulationData', 'total_population', 'working_total_population')
    update_data_in_column('WorkingPopulationData', 'average_wage', 'working_average_wage', operation='mean')
    update_data_in_column('HousingData', 'real_estate_taxes_by_mortgage', 'real_estate_taxes_by_mortgage')
    update_data_in_column('EquityData', 'household_income_by_race', 'household_income')
    update_data_in_column('PovertyData', 'severe_housing_problems', 'severe_housing_problem')
    update_data_in_column('HealthCareData', 'health_insurance_by_gender_and_age', 'health_care_insurance')
    update_data_in_column('ChildMortalityRate', 'child_mortality', 'child_mortality_rate')


def save_health_prosperity_index_in_data():
    """
    This function is used to calculate the final health prosperity index from the selected fields and save the index data
    in YearIndex model
    :return:
    """
    data = HealthProsperityIndexData.objects.all().values("year", "employment_total_population", "working_total_population",
                                                          "real_estate_taxes_by_mortgage", "household_income", "severe_housing_problem",
                                                          "child_mortality_rate", "working_average_wage", "health_care_insurance")
    data = list(data)
    final_data = pd.DataFrame.from_records(data)
    # Normalize each column to a 0-100 scale
    required_columns = final_data.columns.tolist()
    required_columns.remove("year")
    for column in required_columns:  # Skipping the 'Year' column for normalization
        if column == 'child_mortality_rate' or column == 'poverty_rate':
            # Inverse normalization for child mortality and poverty data
            final_data[column] = ((final_data[column].max() - final_data[column]) /
                                  (final_data[column].max() - final_data[column].min())) * 100
        else:
            final_data[column] = ((final_data[column] - final_data[column].min()) /
                                  (final_data[column].max() - final_data[column].min())) * 100

    # Adjust weights to include the new variable: now 8 variables, so each gets a weight of 1/8
    weights_with_wage = np.array([1 / 8] * 8)  # Equal weights for each of the 8 variables

    # Calculate the Health and Prosperity Index with the new variable included
    final_data['Health and Prosperity Index'] = final_data.loc[:, required_columns].dot(weights_with_wage)

    # Assuming 'final_data' is your DataFrame containing the Health and Prosperity Index values for each year
    year_index_dict = {str(year): value for year, value in
                       zip(final_data['year'], final_data['Health and Prosperity Index'])}

    for key, value in year_index_dict.items():
        YearIndexTable.objects.update_or_create(year=key, defaults={"health_prosperity_index": value})


def populate_data_in_database(add=False):
    """
    this function is used to add all the data in database
    :return:
    """
    if add:
        instruction = st.info("Currently there is no data in database. Please wait while we are updating it",
                              icon="ℹ️")
        spinner = st.spinner(text="In progress...")
        with spinner:
            populate_data(add)
            progress_bar.progress(90, text="Updating db 8 out of 9")
            populate_health_index_table()
            progress_bar.progress(100, text="Updating db 9 out of 9")
            save_health_prosperity_index_in_data()
        progress_bar.empty()
        instruction.empty()
        success_text = st.success("Database update complete. Fetching chart", icon="✅")
        time.sleep(2)
        success_text.empty()
    else:
        populate_data()
        populate_health_index_table()
        save_health_prosperity_index_in_data()


if __name__ == '__main__':
    populate_data_in_database()
