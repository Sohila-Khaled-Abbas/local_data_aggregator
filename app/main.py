import streamlit as st
import polars as pl
from processing import process_uploaded_files

st.set_page_config(page_title="Data Aggregator", layout="wide")

st.title("Data Aggregator & Insight Generator")
st.markdown("Upload disparate CSV or Excel files to generate a unified dataset. The aggregator will automatically align differing columns.")

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
            st.subheader("Dataset Overview")
            st.write(f"Total Rows: {final_data.height}")
            st.write(f"Total Columns: {final_data.width}")
            st.write("Column Types:")
            
            # Create a simple dataframe for schema display
            schema_df = pl.DataFrame({
                "Column": final_data.columns,
                "Type": [str(t) for t in final_data.dtypes]
            })
            st.dataframe(schema_df.to_pandas(), hide_index=True, use_container_width=True)
    else:
        st.error("Could not process the uploaded files.")