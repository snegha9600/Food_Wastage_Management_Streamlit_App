import streamlit as st

def app():
    st.title("Local Food Wastage Management System")

    st.markdown("""
    This project helps manage surplus food and reduce wastage by connecting providers with those in need.

    ### Providers:
    Restaurants, households, and businesses list surplus food.

    ### Receivers:
    NGOs and individuals can claim available food.

    ### Geolocation:
    Helps locate nearby food and providers.

    ### SQL Insights:
    Powerful insights using SQL queries for data-driven action.
    """)

    st.info("Use the sidebar to navigate to other sections of the app.")
