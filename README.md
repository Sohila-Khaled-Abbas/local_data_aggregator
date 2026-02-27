<div align="center">

  <!-- Technology Badges -->
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Polars-Fast Data Processing-CD792C?style=for-the-badge&logo=polars&logoColor=white" alt="Polars" />
  <img src="https://img.shields.io/badge/Google_Gemini-AI_Analysis-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />

  <br />
  <br />

  <h1>✨ Data Aggregator AI</h1>
  
  <p>
    <b>Transform your disparate CSV and Excel files into unified, actionable intelligence.</b>
  </p>

  <p>
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#usage">Usage</a>
  </p>

</div>

---

## 📖 Overview

**Data Aggregator AI** is a state-of-the-art data engineering and analysis pipeline paired with a modern, sleek Streamlit dashboard. It enables users to seamlessly upload raw datasets (CSV, XLSX), unify them into a highly optimized matrix using *Polars*, visually explore patterns with *Plotly*, and ultimately generate strategic business recommendations utilizing **Google Gemini LLM**.

---

## 🚀 Features

- **⚡ Blazing Fast Aggregation**: Utilizes `polars` and `fastexcel` to efficiently ingest and process large datasets.
- **🎨 Modern Dark-Mode UI**: A custom-styled, premium aesthetic dashboard providing a seamless user experience.
- **📊 Interactive Visual Analytics**: Out-of-the-box scatter, bar, and line charts generated dynamically based on your data columns using Plotly.
- **🤖 AI-Powered Business Insights**: Automatically runs a statistical profile of your numerical data and queries the Google Gemini Pro model to return actionable recommendations.
- **🐳 Docker Ready**: Instantly spin up the entire environment using the provided Dockerfile.

---

## 🏗️ Project Structure

```text
local_data_aggregator/
├── app/                  # Frontend Streamlit Application
│   ├── main.py           # Dashboard Interface & CSS Injection
│   └── processing.py     # Frontend-to-backend data handling
├── src/                  # Core Data Engineering Logic
│   ├── ingestion.py      # Raw file parsing (CSV, XLSX)
│   ├── transform.py      # Data cleaning and aggregation logic
│   ├── discovery.py      # Schema discovery
│   └── main.py           # Central backend pipeline execution
├── data/                 # Directory for raw user datasets
├── Dockerfile            # Container configuration
└── requirements.txt      # Python dependencies
```

---

## 💻 Getting Started

### Prerequisites

- Python 3.11+ (if running locally)
- [Docker](https://www.docker.com/) (if containerizing)
- A [Google Gemini API Key](https://aistudio.google.com/app/apikey) for AI insights.

### 1. Local Installation

Clone the repository and install the dependencies:

```bash
# 1. Clone repo (or navigate to the directory)
cd local_data_aggregator

# 2. Create a virtual environment
python -m venv venv
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app/main.py
```

### 2. Docker Installation

If you prefer to run the app in an isolated container:

```bash
# Build the Docker image
docker build -t data-aggregator-ai .

# Run the container (Maps port 8501 to localhost)
docker run -p 8501:8501 data-aggregator-ai
```

Access the app at `http://localhost:8501` in your browser.

---

## 💡 Usage

1. **Launch the App**: Open the Streamlit URL provided in your terminal.
2. **Configure AI Setup**: On the left sidebar, enter your **Gemini API Key** to unlock the Intelligence Hub.
3. **Upload Data**: Drag and drop your `.csv` or `.xlsx` files into the core upload zone. The engine will compile an aggregation matrix.
4. **Explore Overview**: Check your dataset's total rows, columns, and estimated size. Use the expander to view the raw unified DataFrame.
5. **Dive into Intelligence**:
   - **📈 Descriptive Statistics**: Review automatically generated quartiles, means, and deviations.
   - **🎨 Visual Analytics**: Create interactive Plotly charts natively in the app.
   - **🤖 AI Business Insights**: Click to generate strategic advice direct from the Gemini model based purely on your dataset’s statistical profile.

---

<div align="center">
  <p><i>Built for the modern data ecosystem.</i></p>
</div>
