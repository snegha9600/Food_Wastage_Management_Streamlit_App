import streamlit as st
from db import run_query

def app():
    st.header("Contact Information")

    # Select contact type
    contact_type = st.selectbox("Select Contact Type", ["Providers", "Receivers"], key="contact_type_select")
    table_name = "providers" if contact_type == "Providers" else "receivers"

    # Fetch distinct cities from the selected table
    city_query = f'SELECT DISTINCT "City" FROM {table_name} ORDER BY "City"'
    try:
        cities = run_query(city_query)
        city_list = [row["City"] for row in cities]
    except Exception as e:
        st.error(f"Error loading cities: {e}")
        return

    # Select a city from the dropdown
    selected_city = st.selectbox("Select City", city_list, key="contact_city_dropdown")

    # Fetch and display contact info based on contact type and selected city
    if selected_city:
        # Adjust query based on available columns
        if table_name == "receivers":
            query = f'SELECT DISTINCT "Name", "Contact" FROM {table_name} WHERE "City" = %s'
        else:
            query = f'SELECT DISTINCT "Name", "Contact", "Address" FROM {table_name} WHERE "City" = %s'

        try:
            results = run_query(query, (selected_city,))
            if results:
                st.dataframe(results)
            else:
                st.warning("No contact information found for the selected city.")
        except Exception as e:
            st.error(f"Error loading contact data: {e}")
