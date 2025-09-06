import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from analysis_month import monthly_analysis_tab

st.title("Expense management system")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics by category", "Analytics by months"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_analysis_tab()