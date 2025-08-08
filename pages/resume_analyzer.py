import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import (
    configure_gemini,
    extract_text_from_pdf,
    format_job_description,
    process_resume,
    screen_resume,
    generate_cumulative_report
)

def render():
    """Renders the Resume Analyzer page."""
    st.title("Resume Analyzer")

    # --- SESSION STATE INITIALIZATION FOR THIS VIEW ---
    if 'resume_analysis_results' not in st.session_state:
        st.session_state.resume_analysis_results = None

    # --- INPUT FORM ---
    with st.form("resume_input_form"):
        st.markdown("Enter the job details and upload resumes to get an AI-powered analysis.")
        col1, col2 = st.columns(2)
        with col1:
            jd_text = st.text_area("Paste the Job Description", height=350)
        with col2:
            uploaded_files = st.file_uploader("Upload Resumes (PDF only)", type="pdf", accept_multiple_files=True)
        submit_button = st.form_submit_button("Analyze Resumes ✨", use_container_width=True)

    # --- ANALYSIS LOGIC ---
    if submit_button:
        if not jd_text or not uploaded_files:
            st.error("🚨 Please provide both the job description and at least one resume.")
        else:
            with st.spinner("Full analysis in progress..."):
                model = configure_gemini()
                # 1. Format JD
                if jd_text.strip().startswith('{'):
                    formatted_jd = jd_text
                else:
                    formatted_jd_dict = format_job_description(jd_text, model)
                    if not formatted_jd_dict:
                        st.error("Could not format the job description.")
                        st.stop()
                    formatted_jd = json.dumps(formatted_jd_dict)

                # 2. Process Resumes and Generate Report
                all_analyses = []
                progress_bar = st.progress(0, "Analyzing resumes...")
                for i, pdf_file in enumerate(uploaded_files):
                    resume_text = extract_text_from_pdf(pdf_file)
                    if resume_text:
                        processed_resume = process_resume(resume_text, model)
                        if processed_resume:
                            analysis = screen_resume(formatted_jd, processed_resume, model)
                            if analysis:
                                analysis['candidate_name'] = processed_resume.get("contact_info", {}).get("name", pdf_file.name)
                                all_analyses.append(analysis)
                    progress_bar.progress((i + 1) / len(uploaded_files), f"Processing {pdf_file.name}")

                # 3. Final Cumulative Report
                if all_analyses:
                    final_report = generate_cumulative_report(all_analyses, model)
                    st.session_state.resume_analysis_results = (final_report, all_analyses)
                    st.balloons()
                else:
                    st.error("No resumes could be processed successfully.")
                    st.session_state.resume_analysis_results = None
                progress_bar.empty()

    # --- DISPLAY RESULTS ---
    if st.session_state.resume_analysis_results:
        display_results()

def display_results():
    """Displays the analysis dashboard and individual deep dive."""
    st.markdown("---")
    st.header("🏆 Analysis Dashboard")
    report_data, analyses_data = st.session_state.resume_analysis_results

    st.subheader("Executive Summary")
    st.info(report_data.get('overall_summary', 'Not available.'))

    df_ranking = pd.DataFrame(report_data.get('candidate_ranking', []))
    if df_ranking.empty:
        st.warning("Could not generate candidate rankings.")
        return

    # --- Key Metrics ---
    col1, col2 = st.columns(2)
    col1.metric("Total Candidates", len(df_ranking))
    col2.metric("Average Match Score", f"{df_ranking['match_score'].mean():.1f}%")
    df_analyses = pd.DataFrame(analyses_data)
    top_rec = df_analyses['final_recommendation'].value_counts()

    # --- Visualizations ---
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Candidate Match Scores")
        fig_bar = px.bar(df_ranking.sort_values(by='match_score'), x='match_score', y='candidate_name', orientation='h', color='match_score', color_continuous_scale='greens', text='match_score')
        fig_bar.update_traces(texttemplate='%{text:.2s}%', textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)
    with col_b:
        st.subheader("Recommendation Distribution")
        fig_pie = px.pie(df_analyses, names='final_recommendation', hole=0.4, color_discrete_map={'Strongly Recommend': '#1a9641', 'Consider': '#a6d96a', 'Not a Fit': '#d7191c'})
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Detailed Ranking Table ---
    st.subheader("Detailed Candidate Ranking")
    st.dataframe(df_ranking.style.background_gradient(cmap='Greens', subset=['match_score']), use_container_width=True)

    # --- NEW: INDIVIDUAL CANDIDATE DEEP DIVE ---
    st.markdown("---")
    st.subheader("Individual Candidate Deep Dive 🔎")

    candidate_names = df_ranking['candidate_name'].tolist()
    selected_candidate = st.selectbox(
        "Select a candidate to view detailed analysis",
        options=candidate_names
    )

    if selected_candidate:
        # Find the detailed analysis for the selected candidate
        details = next((item for item in analyses_data if item.get("candidate_name") == selected_candidate), None)

        if details:
            # Display score and recommendation prominently
            st.markdown(f"#### Analysis for: **{details['candidate_name']}**")
            st.markdown(f"**Score:** `{details['match_score']}%` | **Recommendation:** `{details['final_recommendation']}`")

            # Display summary in an expander
            with st.expander("AI Summary", expanded=True):
                st.write(details.get('summary', 'No summary provided.'))

            # Display strengths and weaknesses
            col_s, col_w = st.columns(2)
            with col_s:
                st.markdown("##### ✅ Strengths")
                strengths = details.get('strengths', ['None listed.'])
                for strength in strengths:
                    st.markdown(f"- {strength}")
            with col_w:
                st.markdown("##### ❌ Weaknesses / Gaps")
                weaknesses = details.get('weaknesses', ['None listed.'])
                for weakness in weaknesses:
                    st.markdown(f"- {weakness}")

            # Display skills analysis in an expander
            with st.expander("Skills Analysis"):
                skills_info = details.get('skills_analysis', {})
                st.markdown("##### Required Skills Found")
                found_skills = skills_info.get('required_skills_found', [])
                st.write(" | ".join(f"`{s}`" for s in found_skills) if found_skills else "None")

                st.markdown("##### Missing Skills")
                missing_skills = skills_info.get('missing_skills', [])
                st.write(" | ".join(f"`{s}`" for s in missing_skills) if missing_skills else "None")