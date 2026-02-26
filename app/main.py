import streamlit as st
import polars as pl
import plotly.express as px
from processing import process_uploaded_files
from openai import OpenAI
import json

st.set_page_config(page_title="Data Aggregator AI", layout="wide", page_icon="✨")

# --- Custom Modern Aesthetic CSS ---
st.markdown("""
<style>
    /* Global Styling */
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #1E293B;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Smooth Inputs & Selectors */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }
    
    /* Sleek Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        color: #f8fafc;
    }

    /* DataFrame custom styling via Streamlit is limited, but we alter the surrounding container */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- App Header ---
st.title("✨ Data Aggregator AI")
st.markdown("Upload disparate CSV or Excel files to generate a unified dataset. Ask our LLM analyst for insights!")

# --- Sidebar configuration for LLM ---
st.sidebar.header("AI Configuration")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", placeholder="sk-...")
st.sidebar.markdown("Provide your OpenAI API key to unlock the **AI Business Insights** tab.")

# --- File Uploader ---
uploaded_files = st.file_uploader(
    "Select files", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Aggregating datasets..."):
        final_data = process_uploaded_files(uploaded_files)
        
    if final_data is not None:
        st.success("Aggregation Complete!")
        
        # --- Overview Section ---
        st.markdown("### 📊 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", final_data.height)
        col2.metric("Columns", final_data.width)
        col3.metric("Data Size", f"{final_data.estimated_size() / 1024:.2f} KB")

        with st.expander("View Full Dataset"):
            st.dataframe(final_data.to_pandas(), use_container_width=True)
            
        st.divider()
        st.header("🔍 Exploratory Data Analysis & AI Insights")
        
        tab1, tab2, tab3 = st.tabs(["📈 Descriptive Statistics", "🎨 Data Visualization", "🤖 AI Business Insights"])
        
        # --- Tab 1: Stats ---
        with tab1:
            st.subheader("Summary Statistics (Numerical Columns)")
            num_cols = [col for col in final_data.columns if final_data[col].dtype in pl.NUMERIC_DTYPES]
            
            if num_cols:
                stats_df = final_data.select(num_cols).describe()
                st.dataframe(stats_df.to_pandas(), use_container_width=True)
            else:
                st.info("No numerical columns found in the unified dataset to generate statistics.")
                
        # --- Tab 2: Visualization ---
        with tab2:
            st.subheader("Interactive Charts")
            chart_type = st.radio("Select Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart"], horizontal=True)
            
            col_x, col_y = st.columns(2)
            with col_x:
                x_axis = st.selectbox("X-Axis", options=final_data.columns)
            with col_y:
                y_axis = st.selectbox("Y-Axis", options=final_data.columns, index=min(1, len(final_data.columns)-1))
                
            pd_df = final_data.to_pandas() 
            
            try:
                # Custom Plotly Template for modern aesthetic
                template = "plotly_white"
                
                if chart_type == "Scatter Plot":
                    fig = px.scatter(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", template=template)
                elif chart_type == "Bar Chart":
                    fig = px.bar(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}", template=template)
                elif chart_type == "Line Chart":
                    fig = px.line(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}", template=template)
                    
                # Enhance traces
                fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not generate {chart_type}. Error: {e}")
                
        # --- Tab 3: AI Insights ---
        with tab3:
            st.subheader("Automated Business Recommendations")
            
            if not openai_api_key:
                st.warning("⚠️ Please provide your OpenAI API Key in the sidebar to use this feature.")
            else:
                if not num_cols:
                    st.info("We need numerical columns to generate statistical business insights.")
                else:
                    if st.button("Generate Insights ✨"):
                        with st.spinner("Analyzing dataset statistics..."):
                            try:
                                client = OpenAI(api_key=openai_api_key)
                                
                                # Prepare data summary for the prompt
                                stat_summary = stats_df.to_pandas().to_json()
                                column_names = ", ".join(final_data.columns)
                                
                                prompt = f"""
                                You are an expert data analyst and business consultant. 
                                I have aggregated a dataset with the following columns: {column_names}.
                                
                                Here are the summary statistics (mean, min, max, std dev, etc.) for the numerical columns in JSON format:
                                {stat_summary}
                                
                                Based on these statistics, provide 3 actionable business recommendations or interesting insights. 
                                Keep your response professional, formatting it beautifully with markdown headers and bullet points. Do not mention the JSON format.
                                """
                                
                                response = client.chat.completions.create(
                                    model="gpt-3.5-turbo",
                                    messages=[
                                        {"role": "system", "content": "You are a professional business data analyst."},
                                        {"role": "user", "content": prompt}
                                    ],
                                    temperature=0.7
                                )
                                
                                st.markdown("### The AI Analyst Says:")
                                st.write(response.choices[0].message.content)
                                
                            except Exception as e:
                                st.error(f"Failed to generate insights via OpenAI: {e}")

    else:
        st.error("Could not process the uploaded files.")