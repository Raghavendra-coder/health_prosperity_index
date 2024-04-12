from pathlib import Path
from add_data import extract_api_data, insert_data, populate_health_index_table, save_health_prosperity_index_in_data
import json
from django.apps import apps
from celery import shared_task
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
json_file_path = BASE_DIR / 'datausa_endpoints.json'


@shared_task()
def update_data_in_database():
    """
    This function will run one time everyday to update the data in the database and graph will provide the latest data
    :return:
    """
    print(f"Updating Database from Latest update on datausa.io at {datetime.now()}")
    updated = False
    try:
        with open(json_file_path) as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    else:
        for value in data.values():
            endpoint = value['endpoint']
            model_name = value['model_name']
            ModelName = apps.get_model(app_label='main_index_app', model_name=model_name)
            data = extract_api_data(endpoint)
            db_object_count = ModelName.objects.count()
            if len(data) != db_object_count:
                #Adding Fresh data if data is modified in Datausa

                ModelName.objects.all().delete()
                insert_data(data, model_name)
                updated = True
    if updated:
        populate_health_index_table()
        save_health_prosperity_index_in_data()
