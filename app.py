# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from pages import resume_analyzer, sentiment_analyzer

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="HR Suite",                 # <-- Changed
    page_icon="🤖",                         # <-- Changed
    layout="wide"
)

# --- HIDE THE DEFAULT SIDEBAR ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# --- Main App ---
class Model:
    def main(self):
        # --- TOP NAVIGATION MENU ---
        with st.container():
            selected = option_menu(
                menu_title=None,
                options=["Resume Analyzer", "Sentiment Analyzer"],
                icons=["person-bounding-box", "bar-chart-line"],
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "#6c757d", "font-size": "20px"},
                    "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # --- RENDER THE SELECTED PAGE ---
        if selected == "Resume Analyzer":
            resume_analyzer.render()
        elif selected == "Sentiment Analyzer":
            sentiment_analyzer.render()

if __name__ == '__main__':
    Model().main()