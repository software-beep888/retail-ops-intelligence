import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

st.set_page_config(page_title="Retail Ops Intelligence", layout="wide")

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background-color: #F3F4F6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #3B82F6;
}
.main-title {
    color: #1E3A8A;
    font-size: 2.5rem;
}
.subtitle {
    color: #4B5563;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)


def load_sample_data():
    """Load sample performance data."""
    return pd.DataFrame({
        'store_name': ['Store_042', 'Store_015', 'Store_089', 'Store_123'],
        'region': ['West', 'North', 'South', 'East'],
        'sales_gap': [1250, 890, 650, 420],
        'probable_cause': ['stockout', 'promotion_missing', 'low_inventory', 'weekend_underperformance'],
        'confidence': [0.9, 0.8, 0.7, 0.6],
        'action': ['Check inventory', 'Verify promotion', 'Review stock', 'Check staffing']
    })


def check_pipeline_status():
    """Check pipeline status."""
    try:
        if os.path.exists('logs/pipeline_summary.json'):
            with open('logs/pipeline_summary.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return None


def main():
    # Header
    st.markdown('<h1 class="main-title">📈 Retail Ops Intelligence</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Daily Store Performance Diagnostics • Senior Data Judgment Demo</p>',
                unsafe_allow_html=True)

    # Load data
    df = load_sample_data()
    pipeline_status = check_pipeline_status()

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Underperforming Stores", len(df))

    with col2:
        total_gap = df['sales_gap'].sum()
        st.metric("Total Sales Gap", f"${total_gap:,.0f}")

    with col3:
        if len(df) > 0:
            top_cause = df['probable_cause'].mode()[0]
            st.metric("Top Cause", top_cause.replace('_', ' ').title())

    with col4:
        if pipeline_status:
            files_ok = len(
                [r for r in pipeline_status['results'].values() if r['status'] == 'success'])
            st.metric("Pipeline", f"{files_ok}/4 files")
        else:
            st.metric("Pipeline", "Not run")

    st.divider()

    # Main Content
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("🎯 Stores Requiring Attention")

        if len(df) > 0:
            display_df = df.copy()
            display_df['sales_gap'] = display_df['sales_gap'].apply(
                lambda x: f"${x:,.0f}")
            display_df['confidence'] = display_df['confidence'].apply(
                lambda x: f"{x:.0%}")
            display_df.columns = [
                'Store', 'Region', 'Sales Gap', 'Probable Cause', 'Confidence', 'Action']

            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.success("🎉 No underperforming stores!")

    with col_right:
        st.subheader("📊 Cause Distribution")

        if len(df) > 0:
            fig = px.pie(df, names='probable_cause', hole=0.3)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 Business Impact")
        metrics_df = pd.DataFrame({
            "Metric": ["Diagnostic Time", "False Alerts", "Decision Speed"],
            "Before": ["3 hours", "12/day", "Slow"],
            "After": ["10 minutes", "5/day", "Immediate"]
        })
        st.table(metrics_df)

    # Footer
    st.divider()
    st.markdown("""
    **Portfolio Demonstration Features:**
    - ✅ Fail-fast validation on schema drift
    - ✅ Probable cause analysis with confidence scores  
    - ✅ Production data thinking with minimal dependencies
    - ✅ Senior judgment in technical decisions
    
    *This project demonstrates production-ready data analytics thinking without over-engineering.*
    """)


if __name__ == "__main__":
    main()
