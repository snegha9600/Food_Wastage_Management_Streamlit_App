import streamlit as st
from db import run_query, load_table_data

def crud_providers():
    st.subheader("Manage Providers")

    df = load_table_data("providers")
    st.dataframe(df)

    st.markdown("### Add Provider")
    with st.form("add_provider"):
        name = st.text_input("Name")
        provider_type = st.text_input("Type")
        contact = st.text_input("Contact")
        address = st.text_input("Address")
        city = st.text_input("City")
        submitted = st.form_submit_button("Add Provider")
        if submitted:
            sql = """
                INSERT INTO providers ("Name", "Type", "Contact", "Address", "City")
                VALUES (%s, %s, %s, %s, %s);
            """
            run_query(sql, (name, provider_type, contact, address, city))
            st.success("Provider added!")

    st.markdown("### Update Provider")
    provider_id = st.number_input("Provider ID to Update", min_value=1, step=1, key="update_provider")
    if st.button("Load Provider"):
        sql = 'SELECT * FROM providers WHERE "Provider_ID" = %s;'
        res = run_query(sql, (provider_id,))
        if res:
            row = res[0]
            name = st.text_input("Name", value=row['Name'], key="update_provider_name")
            provider_type = st.text_input("Type", value=row['Type'], key="update_provider_type")
            contact = st.text_input("Contact", value=row['Contact'], key="update_provider_contact")
            address = st.text_input("Address", value=row['Address'], key="update_provider_address")
            city = st.text_input("City", value=row['City'], key="update_provider_city")

            if st.button("Update Provider"):
                sql = """
                    UPDATE providers
                    SET "Name"=%s, "Type"=%s, "Contact"=%s, "Address"=%s, "City"=%s
                    WHERE "Provider_ID"=%s;
                """
                run_query(sql, (name, provider_type, contact, address, city, provider_id))
                st.success("Provider updated!")

    st.markdown("### Delete Provider")
    del_id = st.number_input("Provider ID to Delete", min_value=1, step=1, key="del_provider_id")
    if st.button("Delete Provider"):
        sql = 'DELETE FROM providers WHERE "Provider_ID" = %s;'
        run_query(sql, (del_id,))
        st.success("Provider deleted!")


def crud_receivers():
    st.subheader("Manage Receivers")

    df = load_table_data("receivers")
    st.dataframe(df)

    st.markdown("### Add Receiver")
    with st.form("add_receiver"):
        name = st.text_input("Name")
        contact = st.text_input("Contact")
        address = st.text_input("Address")
        city = st.text_input("City")
        submitted = st.form_submit_button("Add Receiver")
        if submitted:
            sql = """
                INSERT INTO receivers ("Name", "Contact", "Address", "City")
                VALUES (%s, %s, %s, %s);
            """
            run_query(sql, (name, contact, address, city))
            st.success("Receiver added!")

    st.markdown("### Update Receiver")
    receiver_id = st.number_input("Receiver ID to Update", min_value=1, step=1, key="update_receiver")
    if st.button("Load Receiver"):
        sql = 'SELECT * FROM receivers WHERE "Receiver_ID" = %s;'
        res = run_query(sql, (receiver_id,))
        if res:
            row = res[0]
            name = st.text_input("Name", value=row['Name'], key="update_receiver_name")
            contact = st.text_input("Contact", value=row['Contact'], key="update_receiver_contact")
            address = st.text_input("Address", value=row['Address'], key="update_receiver_address")
            city = st.text_input("City", value=row['City'], key="update_receiver_city")

            if st.button("Update Receiver"):
                sql = """
                    UPDATE receivers
                    SET "Name"=%s, "Contact"=%s, "Address"=%s, "City"=%s
                    WHERE "Receiver_ID"=%s;
                """
                run_query(sql, (name, contact, address, city, receiver_id))
                st.success("Receiver updated!")

    st.markdown("### Delete Receiver")
    del_id = st.number_input("Receiver ID to Delete", min_value=1, step=1, key="del_receiver_id")
    if st.button("Delete Receiver"):
        sql = 'DELETE FROM receivers WHERE "Receiver_ID" = %s;'
        run_query(sql, (del_id,))
        st.success("Receiver deleted!")


def crud_food_listings():
    st.subheader("Manage Food Listings")

    df = load_table_data("food_listings")
    st.dataframe(df)

    st.markdown("### Add Food Listing")
    with st.form("add_food_listing"):
        food_name = st.text_input("Food Name")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        quantity = st.number_input("Quantity", min_value=0)
        expiry_date = st.date_input("Expiry Date")
        provider_id = st.number_input("Provider ID", min_value=1)
        location = st.text_input("Location")
        submitted = st.form_submit_button("Add Food Listing")
        if submitted:
            sql = """
                INSERT INTO food_listings
                ("Food_Name", "Food_Type", "Meal_Type", "Quantity", "Expiry_Date", "Provider_ID", "Location")
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """
            run_query(sql, (food_name, food_type, meal_type, quantity, expiry_date, provider_id, location))
            st.success("Food listing added!")

    st.markdown("### Update Food Listing")
    food_id = st.number_input("Food Listing ID to Update", min_value=1, step=1, key="update_food_listing")
    if st.button("Load Food Listing"):
        sql = 'SELECT * FROM food_listings WHERE "Food_ID" = %s;'
        res = run_query(sql, (food_id,))
        if res:
            row = res[0]
            food_name = st.text_input("Food Name", value=row['Food_Name'], key="update_food_name")
            food_type = st.text_input("Food Type", value=row['Food_Type'], key="update_food_type")
            meal_type = st.text_input("Meal Type", value=row['Meal_Type'], key="update_meal_type")
            quantity = st.number_input("Quantity", value=row['Quantity'], min_value=0, key="update_quantity")
            expiry_date = st.date_input("Expiry Date", value=row['Expiry_Date'], key="update_expiry_date")
            provider_id = st.number_input("Provider ID", value=row['Provider_ID'], min_value=1, key="update_provider_id")
            location = st.text_input("Location", value=row['Location'], key="update_location")

            if st.button("Update Food Listing"):
                sql = """
                    UPDATE food_listings
                    SET "Food_Name"=%s, "Food_Type"=%s, "Meal_Type"=%s, "Quantity"=%s, "Expiry_Date"=%s, "Provider_ID"=%s, "Location"=%s
                    WHERE "Food_ID"=%s;
                """
                run_query(sql, (food_name, food_type, meal_type, quantity, expiry_date, provider_id, location, food_id))
                st.success("Food listing updated!")

    st.markdown("### Delete Food Listing")
    del_id = st.number_input("Food Listing ID to Delete", min_value=1, step=1, key="del_food_listing_id")
    if st.button("Delete Food Listing"):
        sql = 'DELETE FROM food_listings WHERE "Food_ID" = %s;'
        run_query(sql, (del_id,))
        st.success("Food listing deleted!")


def crud_claims():
    st.subheader("Manage Claims")

    df = load_table_data("claims")
    st.dataframe(df)

    st.markdown("### Add Claim")
    with st.form("add_claim"):
        food_id = st.number_input("Food ID", min_value=1)
        receiver_id = st.number_input("Receiver ID", min_value=1)
        status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"])
        timestamp = st.date_input("Timestamp")
        submitted = st.form_submit_button("Add Claim")
        if submitted:
            sql = """
                INSERT INTO claims ("Food_ID", "Receiver_ID", "Status", "Timestamp")
                VALUES (%s, %s, %s, %s);
            """
            run_query(sql, (food_id, receiver_id, status, timestamp))
            st.success("Claim added!")

    st.markdown("### Update Claim")
    claim_id = st.number_input("Claim ID to Update", min_value=1, step=1, key="update_claim")
    if st.button("Load Claim"):
        sql = 'SELECT * FROM claims WHERE "Claim_ID" = %s;'
        res = run_query(sql, (claim_id,))
        if res:
            row = res[0]
            food_id = st.number_input("Food ID", value=row['Food_ID'], min_value=1, key="update_claim_food_id")
            receiver_id = st.number_input("Receiver ID", value=row['Receiver_ID'], min_value=1, key="update_claim_receiver_id")
            status = st.selectbox("Status", ["Pending", "Completed", "Cancelled"], index=["Pending", "Completed", "Cancelled"].index(row['Status']), key="update_claim_status")
            timestamp = st.date_input("Timestamp", value=row['Timestamp'], key="update_claim_timestamp")

            if st.button("Update Claim"):
                sql = """
                    UPDATE claims
                    SET "Food_ID"=%s, "Receiver_ID"=%s, "Status"=%s, "Timestamp"=%s
                    WHERE "Claim_ID"=%s;
                """
                run_query(sql, (food_id, receiver_id, status, timestamp, claim_id))
                st.success("Claim updated!")

    st.markdown("### Delete Claim")
    del_id = st.number_input("Claim ID to Delete", min_value=1, step=1, key="del_claim_id")
    if st.button("Delete Claim"):
        sql = 'DELETE FROM claims WHERE "Claim_ID" = %s;'
        run_query(sql, (del_id,))
        st.success("Claim deleted!")


def app():
    st.title("CRUD Operations")

    options = [
        "Manage Providers",
        "Manage Receivers",
        "Manage Food Listings",
        "Manage Claims"
    ]

    choice = st.sidebar.selectbox("Select CRUD Section", options)

    if choice == "Manage Providers":
        crud_providers()
    elif choice == "Manage Receivers":
        crud_receivers()
    elif choice == "Manage Food Listings":
        crud_food_listings()
    elif choice == "Manage Claims":
        crud_claims()
