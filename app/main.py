import streamlit as st
import polars as pl
import plotly.express as px
from processing import process_uploaded_files
import google.generativeai as genai
import json

st.set_page_config(page_title="Data Aggregator AI", layout="wide", page_icon="✨", initial_sidebar_state="expanded")

# --- Custom Modern Aesthetic CSS ---
st.markdown("""
<style>
    /* Global Styling */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a;
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }
    p {
        color: #cbd5e1 !important;
    }
    
    /* Smooth Inputs & Selectors */
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #334155;
        background-color: #0f172a;
        color: white;
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(168, 85, 247, 0.4);
        color: #f8fafc;
        border: none;
    }

    /* File uploader styling */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #475569;
        border-radius: 12px;
        background-color: #1e293b;
        transition: all 0.3s;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #8b5cf6;
        background-color: rgba(139, 92, 246, 0.1);
    }

    /* DataFrame custom styling via Streamlit is limited, but we alter the surrounding container */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #334155;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #1e293b;
        padding: 10px 20px 0px 20px;
        border-radius: 12px 12px 0 0;
        border: 1px solid #334155;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #cbd5e1;
    }
    .stTabs [aria-selected="true"] {
        color: #a855f7 !important;
        border-bottom: 2px solid #a855f7 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 1rem;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #8b5cf6;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
        font-weight: 600;
    }
    
    /* Insight Card */
    .insight-card {
        background-color: #1e293b;
        border-left: 4px solid #8b5cf6;
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar configuration for LLM ---
st.sidebar.title("⚙️ AI Configuration")
st.sidebar.markdown("Unlock AI-powered business insights by providing your API key.")
gemini_api_key = st.sidebar.text_input("Gemini API Key", type="password", placeholder="AIzaSy...")
st.sidebar.markdown("---")
st.sidebar.markdown("### How it works")
st.sidebar.markdown("1. **Upload** your raw data files.\n2. **Review** the unified dataset and visualizations.\n3. **Generate** AI insights to drive business decisions.")

# --- App Header ---
st.title("✨ Data Aggregator AI")
st.markdown("Transform your disparate CSV and Excel files into unified, actionable intelligence. Upload your data below and let our Gemini AI engine uncover hidden trends.")

# --- File Uploader ---
uploaded_files = st.file_uploader(
    "Drop your datasets here (CSV, XLSX)", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("🧠 Initializing data aggregation matrix..."):
        final_data = process_uploaded_files(uploaded_files)
        
    if final_data is not None:
        st.success("✅ Aggregation Matrix Compiled Successfully!")
        
        # --- Overview Section ---
        st.markdown("### 📊 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        
        col1.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{final_data.height:,}</div>
            <div class="metric-label">Total Rows</div>
        </div>
        """, unsafe_allow_html=True)
        
        col2.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{final_data.width}</div>
            <div class="metric-label">Total Columns</div>
        </div>
        """, unsafe_allow_html=True)
        
        col3.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{final_data.estimated_size() / 1024:.1f}</div>
            <div class="metric-label">Size (KB)</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔍 View Full Unified Dataset", expanded=False):
            st.dataframe(final_data.to_pandas(), use_container_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.header("🔬 Intelligence Hub")
        
        tab1, tab2, tab3 = st.tabs(["📈 Descriptive Statistics", "🎨 Visual Analytics", "🤖 AI Business Insights"])
        
        # --- Tab 1: Stats ---
        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            num_cols = [col for col in final_data.columns if final_data[col].dtype in pl.NUMERIC_DTYPES]
            
            if num_cols:
                stats_df = final_data.select(num_cols).describe()
                st.dataframe(stats_df.to_pandas(), use_container_width=True)
            else:
                st.info("No numerical columns found in the unified dataset to generate statistics.")
                
        # --- Tab 2: Visualization ---
        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_controls, col_chart = st.columns([1, 3])
            
            with col_controls:
                st.markdown("#### Chart Settings")
                chart_type = st.radio("Type", ["Scatter Plot", "Bar Chart", "Line Chart"])
                x_axis = st.selectbox("X-Axis", options=final_data.columns)
                y_axis = st.selectbox("Y-Axis", options=final_data.columns, index=min(1, len(final_data.columns)-1))
                
            with col_chart:
                pd_df = final_data.to_pandas() 
                
                try:
                    # Custom Plotly Template for modern aesthetic (Dark mode to match)
                    template = "plotly_dark"
                    
                    if chart_type == "Scatter Plot":
                        fig = px.scatter(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}", template=template)
                    elif chart_type == "Bar Chart":
                        fig = px.bar(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}", template=template)
                    elif chart_type == "Line Chart":
                        fig = px.line(pd_df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}", template=template)
                        
                    # Enhance traces and background
                    fig.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter, sans-serif")
                    )
                    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not generate {chart_type}. Error: {e}")
                
        # --- Tab 3: AI Insights ---
        with tab3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 🧠 Automated Business Recommendations")
            
            if not gemini_api_key:
                st.markdown("""
                <div class="insight-card">
                    <strong>⚠️ Authentication Required</strong><br>
                    Please provide your Gemini API Key in the sidebar configuration to unlock AI-powered insights.
                </div>
                """, unsafe_allow_html=True)
            else:
                if not num_cols:
                    st.info("We need numerical columns to generate statistical business insights.")
                else:
                    st.markdown("Send your dataset's statistical profile to our LLM to generate strategic recommendations.")
                    if st.button("Generate Strategic Insights ✨"):
                        with st.spinner("Analyzing statistical matrix and generating report..."):
                            try:
                                # Configure Gemini API safely per run
                                genai.configure(api_key=gemini_api_key)
                                
                                # Use Gemini Pro model
                                model = genai.GenerativeModel('gemini-pro')
                                
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
                                
                                response = model.generate_content(prompt)
                                
                                st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
                                st.markdown("### The AI Analyst Says:")
                                st.write(response.text)
                                st.markdown("</div>", unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.error(f"Failed to generate insights via Google Gemini: {e}")

    else:
        st.error("Could not process the uploaded files.")