import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"


def monthly_analysis_tab():
    st.header("Monthly Expense Analysis")

    try:
        response = requests.get(f"{API_URL}/monthly-analytics/")

        if response.status_code == 200:
            monthly_data = response.json()

            if monthly_data:
                df = pd.DataFrame(monthly_data)


                st.subheader("Total Expenses by Month")
                st.bar_chart(data=df, x="month", y="total", use_container_width=True)

                st.subheader("Detailed Monthly Breakdown")
                df_display = df.copy()
                df_display["total"] = df_display["total"].map("${:.2f}".format)
                st.table(df_display)
            else:
                st.warning("No monthly data available. Add some expenses first.")
        else:
            st.error("Failed to retrieve monthly analytics")

    except Exception as e:
        st.error(f"Error connecting to server: {str(e)}")