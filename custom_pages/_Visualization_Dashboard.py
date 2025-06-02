import streamlit as st
import pandas as pd
import plotly.express as px
from db import run_query

def app():
    st.header("Visualization Dashboard")

    # Bar chart: Providers per City
    query_providers_city = """
        SELECT "City", COUNT(*) AS provider_count
        FROM providers
        GROUP BY "City"
        ORDER BY provider_count DESC;
    """
    df_providers_city = pd.DataFrame(run_query(query_providers_city), columns=["City", "provider_count"])

    fig_bar = px.bar(df_providers_city, x="City", y="provider_count", 
                     title="Providers per City", labels={"City": "City", "provider_count": "Number of Providers"})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart: Provider Types distribution
    query_provider_types = """
        SELECT "Provider_Type", SUM("Quantity") AS total_quantity
        FROM food_listings
        GROUP BY "Provider_Type"
        ORDER BY total_quantity DESC;
    """
    df_provider_types = pd.DataFrame(run_query(query_provider_types), columns=["Provider_Type", "total_quantity"])

    fig_pie = px.pie(df_provider_types, values='total_quantity', names='Provider_Type',
                     title="Food Quantity by Provider Type")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Line chart: Weekly Claim Trends
    query_weekly_claims = """
        SELECT DATE_TRUNC('week', "Timestamp") AS week_start, COUNT(*) AS total_claims
        FROM claims
        GROUP BY week_start
        ORDER BY week_start;
    """
    df_weekly_claims = pd.DataFrame(run_query(query_weekly_claims), columns=["week_start", "total_claims"])
    df_weekly_claims['week_start'] = pd.to_datetime(df_weekly_claims['week_start'])

    fig_line = px.line(df_weekly_claims, x='week_start', y='total_claims', 
                       title="Weekly Claim Trends", labels={"week_start": "Week Starting", "total_claims": "Total Claims"})
    st.plotly_chart(fig_line, use_container_width=True)
