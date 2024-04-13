import altair as alt
import requests
import pandas as pd
import streamlit as st
import time
from add_data import populate_data_in_database
from django.conf import settings
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from main_index_app.models import *


def get_index_df():
    """
    Fetch final index data from database and returns in form of pandas dataframe
    """
    if settings.LOCAL:
        base_url = settings.LOCAL_BASE_URL
    else:
        base_url = settings.DEPLOYED_BASE_URL
    endpoint = f"{base_url}/main/api/v1/get_final_index"
    response = requests.get(endpoint)
    success_text = None
    if response.status_code == 200:
        response_json = response.json()
        if not response_json['success']:
            populate_data_in_database(add=True)
            success_text = st.success("Database update complete. Fetching chart", icon="✅")
            time.sleep(1)

            response = requests.get(endpoint)
            if not response.status_code == 200:
                return False, None, success_text
            response_json = response.json()

        final_data_with_index = pd.DataFrame(response_json["data"]).rename(
                columns={"year": "Year", "health_prosperity_index": "Health and Prosperity Index"})
        return True, final_data_with_index, success_text
    return False, None, success_text


def get_health_prosperity_index_graph():
    """
        This function is used to get the details from the database and calculate the final health and prosperity Index of
        the latest data
    """
    try:
        # Pass the request object to the view associated with your API endpoint
        success, index_df, success_text = get_index_df()
        if success:
            base = alt.Chart(index_df, title="Health and Prosperity Index").encode(
                x='Year',
                y='Health and Prosperity Index',
                tooltip=['Year', 'Health and Prosperity Index'],
            )
            line = base.mark_line()
            points = base.mark_point(filled=True, size=80)
            chart = (line + points).interactive()
            if success_text:
                success_text.empty()
            # Render the chart in Streamlit
            st.altair_chart(chart, use_container_width=True, )

            st.dataframe(index_df.loc[:, ['Year', 'Health and Prosperity Index']])
        else:
            st.error("Could not fetch data from database. please refresh to try again", icon="🚨")

    except Exception as e:
        st.error(f"Sorry unable to process the graph due to some exception in our system. Thanks for your patience {e}",
                 icon="🚨")


def clear_database():

    EmploymentData.objects.all().delete()
    WorkingPopulationData.objects.all().delete()
    HousingData.objects.all().delete()
    EquityData.objects.all().delete()
    HealthCareData.objects.all().delete()
    PovertyData.objects.all().delete()
    ChildMortalityRate.objects.all().delete()
    HealthProsperityIndexData.objects.all().delete()
    YearIndexTable.objects.all().delete()


if __name__ == '__main__':
    get_health_prosperity_index_graph()
    sidebar = st.sidebar
    if sidebar.button("Clear database to test again"):
        clear_database()
        st.toast("Database has been cleared. Please refresh  the page to test again.")
        st.stop()

