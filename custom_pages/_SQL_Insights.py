import streamlit as st
from db import run_query
import pandas as pd

SQL_QUERIES = {
    # A. Providers & Receivers
    "1. Count of Providers per City": """
        SELECT "City", COUNT(*) AS provider_count
        FROM providers
        GROUP BY "City"
        ORDER BY provider_count DESC;
    """,
    "2. Count of Receivers per City": """
        SELECT "City", COUNT(*) AS receiver_count
        FROM receivers
        GROUP BY "City"
        ORDER BY receiver_count DESC;
    """,
    "3. Top Contributing Provider Types": """
        SELECT "Provider_Type", SUM("Quantity") AS total_quantity
        FROM food_listings
        GROUP BY "Provider_Type"
        ORDER BY total_quantity DESC;
    """,
    "4. Contact Info of Providers in a City (Replace 'YourCityName')": """
        SELECT "Name", "Contact", "Address"
        FROM providers
        WHERE "City" = 'YourCityName';
    """,
    "5. Receivers with Most Food Claims": """
        SELECT r."Name", COUNT(c."Claim_ID") AS total_claims
        FROM claims c
        JOIN receivers r ON c."Receiver_ID" = r."Receiver_ID"
        GROUP BY r."Name"
        ORDER BY total_claims DESC
        LIMIT 5;
    """,
    "6. Number of Providers by Type": """
        SELECT "Type", COUNT(*) AS provider_count
        FROM providers
        WHERE "Type" IS NOT NULL AND "Type" <> ''
        GROUP BY "Type"
        ORDER BY provider_count DESC;
    """,
    "7. Most Active Provider (by number of listings)": """
        SELECT p."Name", COUNT(f."Food_ID") AS total_listings
        FROM food_listings f
        JOIN providers p ON f."Provider_ID" = p."Provider_ID"
        GROUP BY p."Name"
        ORDER BY total_listings DESC
        LIMIT 1;
    """,

    # B. Listings & Availability
    "8. Total Available Food Quantity": """
        SELECT 'Total' AS label, SUM("Quantity") AS total_available_quantity
        FROM food_listings;

    """,
    "9. Cities with Most Listings": """
        SELECT "Location", COUNT(*) AS listing_count
        FROM food_listings
        GROUP BY "Location"
        ORDER BY listing_count DESC;
    """,
    "10. Most Common Food Types": """
        SELECT "Food_Type", COUNT(*) AS count
        FROM food_listings
        GROUP BY "Food_Type"
        ORDER BY count DESC;
    """,
    "11. Available Meals by Type": """
        SELECT "Meal_Type", COUNT(*) AS meal_count
        FROM food_listings
        GROUP BY "Meal_Type"
        ORDER BY meal_count DESC;
    """,
    "12. Average Quantity of Food per Listing": """
        SELECT AVG("Quantity") AS avg_quantity
        FROM food_listings;
    """,
    "13. Listings Nearing Expiry (next 3 days)": """
        SELECT "Food_Name", "Expiry_Date"
        FROM food_listings
        WHERE "Expiry_Date" <= CURRENT_DATE + INTERVAL '3 days';
    """,

    # C. Claims & Distribution
    "14. Number of Claims per Food Item": """
        SELECT f."Food_Name", COUNT(c."Claim_ID") AS claim_count
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        GROUP BY f."Food_Name"
        ORDER BY claim_count DESC;
    """,
    "15. Provider with Most Completed Claims": """
        SELECT p."Name", COUNT(c."Claim_ID") AS completed_claims
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        JOIN providers p ON f."Provider_ID" = p."Provider_ID"
        WHERE c."Status" = 'Completed'
        GROUP BY p."Name"
        ORDER BY completed_claims DESC;
    """,
    "16. Claim Status Percentages": """
        SELECT "Status", ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) AS percentage
        FROM claims
        GROUP BY "Status";
    """,
    "17. Most Claimed Food Types": """
        SELECT f."Food_Type", COUNT(c."Claim_ID") AS claim_count
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        GROUP BY f."Food_Type"
        ORDER BY claim_count DESC;
    """,
    "18. Receivers Who Cancel Claims Often": """
        SELECT r."Name", COUNT(*) AS cancelled_claims
        FROM claims c
        JOIN receivers r ON c."Receiver_ID" = r."Receiver_ID"
        WHERE c."Status" = 'Cancelled'
        GROUP BY r."Name"
        ORDER BY cancelled_claims DESC;
    """,
    "19. Food Items with Most Cancelled Claims": """
        SELECT f."Food_Name", COUNT(*) AS cancelled_claims
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        WHERE c."Status" = 'Cancelled'
        GROUP BY f."Food_Name"
        ORDER BY cancelled_claims DESC;
    """,

    # D. Analysis & Insights
    "20. Average Food Quantity Claimed per Receiver": """
        SELECT r."Name", AVG(f."Quantity") AS avg_quantity
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        JOIN receivers r ON c."Receiver_ID" = r."Receiver_ID"
        GROUP BY r."Name"
        ORDER BY avg_quantity DESC;
    """,
    "21. Most Claimed Meal Type": """
        SELECT f."Meal_Type", COUNT(c."Claim_ID") AS claim_count
        FROM claims c
        JOIN food_listings f ON c."Food_ID" = f."Food_ID"
        GROUP BY f."Meal_Type"
        ORDER BY claim_count DESC;
    """,
    "22. Total Food Donated by Each Provider": """
        SELECT p."Name", SUM(f."Quantity") AS total_donated
        FROM food_listings f
        JOIN providers p ON f."Provider_ID" = p."Provider_ID"
        GROUP BY p."Name"
        ORDER BY total_donated DESC;
    """,
    "23. Expiry Risk: Food Expiring Soon (within 7 days)": """
        SELECT "Food_Name", "Expiry_Date"
        FROM food_listings
        WHERE "Expiry_Date" BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days';
    """,
    "24. Weekly Claim Trends": """
        SELECT DATE_TRUNC('week', "Timestamp") AS week_start, COUNT(*) AS total_claims
        FROM claims
        GROUP BY week_start
        ORDER BY week_start;
    """,
    "25. Monthly Claim Trends": """
        SELECT DATE_TRUNC('month', "Timestamp") AS month, COUNT(*) AS total_claims
        FROM claims
        GROUP BY month
        ORDER BY month;
    """
}

def app():
    st.header("SQL Query Insights")

    query_name = st.selectbox("Select Query to Run", list(SQL_QUERIES.keys()))

    # Pre-input field for city name if required
    city = None
    if query_name == "4. Contact Info of Providers in a City (Replace 'YourCityName')":
        city = st.text_input("Enter City Name")

    if st.button("Run Query"):
        sql = SQL_QUERIES[query_name]

        if query_name == "4. Contact Info of Providers in a City (Replace 'YourCityName')":
            if city:
                # Use ILIKE for case-insensitive match (more user-friendly)
                sql = """
                    SELECT DISTINCT "Name", "Contact", "Address"
                    FROM providers
                    WHERE "City" ILIKE %s;
                """
                result = run_query(sql, (city,))
                st.write(pd.DataFrame(result))
            else:
                st.warning("Please enter a city name to run this query.")
        else:
            result = run_query(sql)
            st.write(pd.DataFrame(result))
