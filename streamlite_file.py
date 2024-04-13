import requests
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from django.conf import settings
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()


def get_health_prosperity_index_graph():
    """
        This function is used to get the details from the database and calculate the final health and prosperity Index of
        the latest data
        :return:
        """
    try:
        # Pass the request object to the view associated with your API endpoint
        if settings.LOCAL:
            base_url = settings.LOCAL_BASE_URL
        else:
            base_url = settings.DEPLOYED_BASE_URL
        endpoint = f"{base_url}/main/api/v1/get_final_index"
        response = requests.get(endpoint)

        if response.status_code == 200:  # Check the status code of the response
            data = response.json()

            final_data_with_index = pd.DataFrame(data["data"]).rename(columns={"year": "Year", "health_prosperity_index": "Health and Prosperity Index"})

            base = alt.Chart(final_data_with_index, title="Health and Prosperity Index").encode(
                x='Year',
                y='Health and Prosperity Index',
                tooltip=['Year', 'Health and Prosperity Index'],
            )
            line = base.mark_line()
            points = base.mark_point(filled=True, size=80)
            chart = (line + points).interactive()

            # Render the chart in Streamlit
            st.altair_chart(chart, use_container_width=True)

            st.dataframe(final_data_with_index.loc[:, ['Year', 'Health and Prosperity Index']])
        else:
            st.write(f"API response error {response.json()}")

    except Exception as e:
        st.write("Sorry unable to process the graph due to some exception in our system. Thanks for your patience", e)


if __name__ == '__main__':
    get_health_prosperity_index_graph()