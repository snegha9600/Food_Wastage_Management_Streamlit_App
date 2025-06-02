# Local Food Wastage Management System

A Streamlit-based web app to reduce food wastage by connecting surplus food providers (like restaurants and stores) with receivers (NGOs and individuals in need). Built with Python, SQL, and Streamlit.

---

## Features

- Stores and manages food donation data using SQL
- Displays insights from 25 SQL queries
- Filters by city, provider, food/meal type
- CRUD operations for providers, receivers, food listings and claims
- Contact details for coordination
- Deployed on Streamlit Cloud

---

## 📁 Datasets Used

- `providers_data.csv` – Info about food providers
- `receivers_data.csv` – Info about food receivers
- `food_listings_data.csv` – Available food items
- `claims_data.csv` – Food claim history

---

## 📊 Sample Questions Answered

- Which city has the most food listings?
- What’s the most claimed meal type?
- Who are the top donors and receivers?
- Claim completion rates and trends

---

## 🛠️ Tech Stack

- Python • Streamlit • SQL • Pandas • GitHub

---

## ▶️ Run Locally

```bash
git clone https://github.com/yourusername/food-wastage-management.git
cd food-wastage-management
pip install -r requirements.txt
streamlit run app.py
