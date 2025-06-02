import streamlit as st
import pandas as pd
from db import run_query

def normalize_keys(data):
    """Convert all keys in each dict row to lowercase for consistency."""
    return [{k.lower(): v for k, v in row.items()} for row in data]

def app():
    st.header("Data Explorer")

    table = st.selectbox("Select Data to Explore", ["Food Listings", "Claims"])

    if table == "Food Listings":
        st.subheader("Filter Food Donations")

    # Dropdown for Location
    locations = run_query('SELECT DISTINCT "Location" FROM "food_listings"')
    location_options = [""] + [row["Location"] for row in locations] if locations else [""]
    location = st.selectbox("Filter by Location", location_options)

    # Dropdown for Provider Name
    providers = run_query('''
        SELECT DISTINCT p."Name" 
        FROM "food_listings" f 
        JOIN "providers" p ON f."Provider_ID" = p."Provider_ID"
    ''')
    provider_options = [""] + [row["Name"] for row in providers] if providers else [""]
    provider_name = st.selectbox("Filter by Provider Name", provider_options)

    # Food Type and Meal Type
    food_type = st.selectbox("Filter by Food Type", ["", "Vegetarian", "Non-Vegetarian", "Vegan"])
    meal_type = st.selectbox("Filter by Meal Type", ["", "Breakfast", "Lunch", "Dinner", "Snacks"])

    # Build the base query
    query = '''
        SELECT f."Food_ID", f."Food_Name", f."Quantity", f."Expiry_Date",
               f."Location", f."Food_Type", f."Meal_Type",
               p."Name" AS provider_name, p."Contact" AS provider_contact
        FROM "food_listings" f
        LEFT JOIN "providers" p ON f."Provider_ID" = p."Provider_ID"
    '''

    # Add WHERE clauses dynamically
    filters = []
    params = []

    if location:
        filters.append('f."Location" = %s')
        params.append(location)
    if provider_name:
        filters.append('p."Name" = %s')
        params.append(provider_name)
    if food_type:
        filters.append('f."Food_Type" = %s')
        params.append(food_type)
    if meal_type:
        filters.append('f."Meal_Type" = %s')
        params.append(meal_type)

    # Add filter conditions to query
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Apply filters only when the button is clicked
    if st.button("Apply Filters"):
        data = run_query(query, tuple(params) if params else None)

        if data:
            normalized_data = normalize_keys(data)
            df = pd.DataFrame(normalized_data).drop_duplicates()
            st.dataframe(df)
        else:
            st.info("No matching food listings found.")