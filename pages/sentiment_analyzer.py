import streamlit as st
import pandas as pd
from utils import configure_gemini, analyze_employee_sentiment

def render():
    """Renders the Sentiment Analyzer page."""
    st.title("Employee Sentiment Analyzer ")

    st.markdown("""
    Upload an Excel sheet with employee feedback to generate an AI-powered sentiment analysis report.
    The report will identify key themes, assess attrition risk, and provide actionable recommendations.
    """)

    # --- File Uploader ---
    uploaded_file = st.file_uploader(
        "Upload your Employee Responses Excel File",
        type=['xlsx'],
        help="The Excel file should contain columns with employee feedback."
    )

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("File Uploaded Successfully!")
            st.markdown("### Data Preview")
            st.dataframe(df.head())

            # --- Analysis Button ---
            if st.button("Analyze Sentiment ✨", use_container_width=True):
                with st.spinner("Analyzing feedback... This may take a few moments. "):
                    model = configure_gemini()
                    if model:
                        report = analyze_employee_sentiment(df, model)
                        st.markdown("---")
                        st.markdown("## Sentiment Analysis Report")
                        st.markdown(report)
                    else:
                        st.error("Failed to configure the AI model. Please check your API key.")

        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")