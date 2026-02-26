import streamlit as st
import polars as pl
from processing import process_uploaded_files

st.set_page_config(page_title="Data Aggregator", layout="wide")

st.title("Data Aggregator & Insight Generator")
st.markdown("Upload disparate CSV or Excel files with `Date`, `Revenue`, and `Region` columns to generate a unified report.")

uploaded_files = st.file_uploader(
    "Select files", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Aggregating datasets..."):
        final_data = process_uploaded_files(uploaded_files)
        
    if final_data is not None:
        st.success("Aggregation Complete.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Unified Dataset")
            st.dataframe(final_data.to_pandas(), use_container_width=True)
            
        with col2:
            st.subheader("Revenue by Region")
            # Grouping in Polars, then plotting in Streamlit
            region_summary = final_data.group_by("Region").agg(pl.col("Revenue").sum())
            st.bar_chart(region_summary.to_pandas().set_index("Region"))
    else:
        st.error("Could not process the uploaded files. Please check the data schema.")