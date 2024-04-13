import requests
import pandas as pd
import streamlit as st
import altair as alt
from add_data import populate_data_in_database
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from django.conf import settings


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

    if response.status_code == 200:
        response_json = response.json()
        print(response_json, "111111111")
        if not response_json['success']:
            populate_data_in_database(add=True)
            response = requests.get(endpoint)
            if not response.status_code == 200:
                return False, None
            response_json = response.json()
            print(response_json, "222222222222")
            st.write(response_json)

        final_data_with_index = pd.DataFrame(response_json["data"]).rename(
                columns={"year": "Year", "health_prosperity_index": "Health and Prosperity Index"})
        return True, final_data_with_index
    return False, None


def get_health_prosperity_index_graph():
    """
        This function is used to get the details from the database and calculate the final health and prosperity Index of
        the latest data
    """
    try:
        # Pass the request object to the view associated with your API endpoint
        success, index_df = get_index_df()
        if success:
            base = alt.Chart(index_df, title="Health and Prosperity Index").encode(
                x='Year',
                y='Health and Prosperity Index',
                tooltip=['Year', 'Health and Prosperity Index'],
            )
            line = base.mark_line()
            points = base.mark_point(filled=True, size=80)
            chart = (line + points).interactive()

            # Render the chart in Streamlit
            st.altair_chart(chart, use_container_width=True, )
            st.divider()
            st.dataframe(index_df.loc[:, ['Year', 'Health and Prosperity Index']])
        else:
            st.error("Could not fetch data from database. please refresh to try again", icon="🚨")

    except Exception as e:
        st.error(f"Sorry unable to process the graph due to some exception in our system. Thanks for your patience {e}",
                 icon="🚨")


if __name__ == '__main__':
    # from main_index_app.models import *
    get_health_prosperity_index_graph()