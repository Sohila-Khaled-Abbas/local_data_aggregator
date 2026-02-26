import streamlit as st
import polars as pl
import plotly.express as px
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
            
        st.divider()
        st.header("Exploratory Data Analysis")
        
        tab1, tab2 = st.tabs(["Descriptive Statistics", "Data Visualization"])
        
        with tab1:
            st.subheader("Summary Statistics (Numerical Columns)")
            # Get numerical columns
            num_cols = [col for col in final_data.columns if final_data[col].dtype in pl.NUMERIC_DTYPES]
            
            if num_cols:
                # Polars describe() provides count, null_count, mean, std, min, 25%, 50%, 75%, max
                stats_df = final_data.select(num_cols).describe()
                st.dataframe(stats_df.to_pandas(), use_container_width=True)
            else:
                st.info("No numerical columns found in the unified dataset to generate statistics.")
                
        with tab2:
            st.subheader("Interactive Charts")
            
            # Allow user to select chart type and axes
            chart_type = st.radio("Select Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart"], horizontal=True)
            
            col_x, col_y = st.columns(2)
            with col_x:
                x_axis = st.selectbox("X-Axis", options=final_data.columns)
            with col_y:
                y_axis = st.selectbox("Y-Axis", options=final_data.columns, index=min(1, len(final_data.columns)-1))
                
            # Render chart based on selections using Plotly
            pd_df = final_data.to_pandas() # Plotly Express works best with Pandas
            
            try:
                if chart_type == "Scatter Plot":
                    fig = px.scatter(pd_df, x=x_axis, y=y_axis, title=f"Scatter Plot: {y_axis} vs {x_axis}")
                elif chart_type == "Bar Chart":
                    fig = px.bar(pd_df, x=x_axis, y=y_axis, title=f"Bar Chart: {y_axis} by {x_axis}")
                elif chart_type == "Line Chart":
                    fig = px.line(pd_df, x=x_axis, y=y_axis, title=f"Line Chart: {y_axis} over {x_axis}")
                    
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not generate {chart_type}. Please ensure the selected columns are compatible with this chart type. Error: {e}")
                
    else:
        st.error("Could not process the uploaded files.")