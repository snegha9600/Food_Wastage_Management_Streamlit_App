import streamlit as st
from config import NAV_OPTIONS
import importlib

# Map page names to module paths
PAGE_MAP = {
    "Project Introduction": "custom_pages._Project_Intro",
    "Data Explorer": "custom_pages._Data_Explorer",
    "CRUD Operations": "custom_pages._CRUD_Operations",
    "SQL Query Insights": "custom_pages._SQL_Insights",
    "Visualization Dashboard": "custom_pages._Visualization_Dashboard",
    "Contact Info": "custom_pages._Contact_Info"
}

def main():
    st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

    # Only the Navigate radio in sidebar
    choice = st.sidebar.radio("Navigate", NAV_OPTIONS)

    # Load and run the selected module
    module_path = PAGE_MAP.get(choice)
    if not module_path:
        st.error(f"Page '{choice}' not found.")
        return

    try:
        page_module = importlib.import_module(module_path)
        if hasattr(page_module, "app"):
            page_module.app()
        else:
            st.error(f"The module '{module_path}' does not have an app() function.")
    except Exception as e:
        st.error(f"Failed to load module: {e}")

if __name__ == "__main__":
    main()