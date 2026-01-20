import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Identity Dashboard", page_icon="🆔", layout="wide")

st.title("🆔 Analytics & Identity Dashboard")
st.markdown("---")
st.markdown("""
> *System Overview:* This AI-powered dashboard detects *identity fraud* in real-time. 
> It analyzes biometric match scores and flags suspicious users falling below the security threshold.
""")
# ---------------------------------------------------------
# 2. Sidebar & Data Loading
# ---------------------------------------------------------
st.sidebar.header("📂 Data Settings")

uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Custom File Loaded!")
elif os.path.exists("data/demographic.csv"):
    df = pd.read_csv("data/demographic.csv")
    st.sidebar.info("ℹ️ Loading local 'demographic.csv'")
else:
     st.sidebar.warning("⚠️ No CSV found! Using Dummy Data.")
     data = {
        'Age': [25, 30, 22, 35, 40, 29, 45, 28, 33, 21, 50, 38, 27, 44, 31],
        'Gender': ['Male', 'Female', 'Male', 'Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
        'Region': ['North', 'South', 'North', 'West', 'South', 'East', 'North', 'West', 'East', 'South', 'North', 'West', 'East', 'South', 'North'],
        'Score': [88, 92, 75, 81, 95, 89, 78, 85, 60, 91, 82, 77, 69, 94, 73]
    }
     df = pd.DataFrame(data)

# ---------------------------------------------------------
# 3. Sidebar Filters
# ---------------------------------------------------------
# Region Filter
region_list = df['Region'].unique().tolist()
region_filter = st.sidebar.multiselect("Select Region", options=region_list, default=region_list)

# Filter Logic
df_selection = df.query("Region == @region_filter")

# ---------------------------------------------------------
# 4. KPI Metrics (Top Row)
# (PASTE THIS)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="👥 Total Identities Verified", value=len(df_selection), delta="12 New Cases")

with col2:
    avg_score = df_selection['Score'].mean()
    st.metric(label="⭐ Avg Biometric Match Score", value=f"{avg_score:.2f}", delta=f"{(avg_score - 85):.1f}% vs Target", delta_color="normal")

with col3:
    risk_count = len(df_selection[df_selection['Score'] < 75])
    st.metric(label="🚨 High Risk Alerts", value=risk_count, delta="Action Required", delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------
# 5. CHARTS SECTION (The Main Changes)
# ---------------------------------------------------------
st.subheader("📊 Performance & Gender Analysis")

c1, c2 = st.columns(2)

# --- CHART 1: Age vs Score (Real-time Problem Finding) ---
with c1:
    st.markdown("### 🔍 Age vs  Biometric Match Score ")
    # Heatmap
    fig_scatter = px.scatter(
        df_selection,
        x='Age',
        y='Score',
        color='Gender',           
        size='Score',               
        hover_data=['Region'],
        title="⚠️ Identity Risk Distribution (Hover for Bio-Data)"
    )
    # Custom Tooltip: 
    fig_scatter.update_traces(
        hovertemplate="<b>Age: %{x}</b><br>Score: %{y}<br>Region: %{customdata[0]}<extra></extra>"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- CHART 2: Gender vs Score (Box Plot) ---
with c2:
    st.markdown("### ⚖️ Gender Score Distribution")
    
    fig_gender = px.box(
        df_selection, 
        x='Gender', 
        y='Score', 
        color='Gender',
        points="all",   # "all
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# ---------------------------------------------------------
# 6. DETAILED PROBLEM LIST (New Feature)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🚨 Problem Detection Area")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.info("select from the slider below the score threshold for marking as problem")
    # Slider to set threshold
    threshold = st.slider("Select Passing Score Threshold", 0, 100, 75)

# Filter data based on slider
problem_data = df_selection[df_selection['Score'] < threshold]

with col_right:
    with col_right:
        if not problem_data.empty:
            # 1. MESSAGE CHANGE:  "Student" से "Fraud Alert" 
            st.error(f"🚨 SECURITY ALERT: {len(problem_data)} Suspicious Identities Detected (Score < {threshold})")
            
            # Data table 
            st.dataframe(
                problem_data.style.background_gradient(cmap="Reds", subset=["Score"]),
                use_container_width=True
            )
            
            
            csv = problem_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Suspicious Report",
                data=csv,
                file_name='suspicious_activity_report.csv',
                mime='text/csv',
            )
        else:
            st.success("✅ System Secure: No suspicious activity found.")
            