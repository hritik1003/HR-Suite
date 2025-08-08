import streamlit as st
from streamlit_option_menu import option_menu
from pages import resume_analyzer, sentiment_analyzer
from typing import Callable, Dict

# --- Constants ---
# Define constants for page configuration and styling to avoid "magic strings"
# and make future updates easier.
PAGE_CONFIG = {
    "page_title": "HR Suite",
    "page_icon": "🤖",
    "layout": "wide"
}

MENU_STYLES = {
    "container": {"padding": "0!important", "background-color": "#fafafa"},
    "icon": {"color": "#6c757d", "font-size": "20px"},
    "nav-link": {
        "font-size": "16px",
        "text-align": "center",
        "margin": "0px",
        "--hover-color": "#eee",
    },
    "nav-link-selected": {"background-color": "#02ab21"},
}

# --- Page Configuration ---
# Set the page configuration. This must be the first Streamlit command.
st.set_page_config(**PAGE_CONFIG)


def apply_custom_styles():
    """
    Applies custom CSS to hide the default Streamlit sidebar,
    as this app uses a custom horizontal navigation menu.
    """
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)


def get_page_router() -> Dict[str, Callable]:
    """
    Returns a dictionary that maps page names to their rendering functions.
    This "router" approach is scalable and cleaner than multiple if/elif statements.
    
    Returns:
        Dict[str, Callable]: A dictionary where keys are page names and
                             values are the functions to render those pages.
    """
    return {
        "Resume Analyzer": resume_analyzer.render,
        "Sentiment Analyzer": sentiment_analyzer.render,
    }


def main():
    """
    Main function to run the Streamlit application.
    """
    apply_custom_styles()
    
    # Get the page router and available page names.
    page_router = get_page_router()
    page_names = list(page_router.keys())

    # Display the top navigation menu.
    with st.container():
        selected_page = option_menu(
            menu_title=None,
            options=page_names,
            # Icons from: https://icons.getbootstrap.com/
            icons=["person-bounding-box", "bar-chart-line"],
            orientation="horizontal",
            styles=MENU_STYLES
        )

    # Render the selected page by calling its associated function from the router.
    if selected_page in page_router:
        page_router[selected_page]()


# --- Application Entry Point ---
if __name__ == '__main__':
    main()