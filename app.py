import streamlit as st
from streamlit_option_menu import option_menu

from modules.dashboard import dashboard_page
from modules.add_trade import add_trade_page
from modules.journal import journal_page
from modules.calendar_view import calendar_page
from modules.analytics import analytics_page
from modules.edge_analyzer import edge_page


st.set_page_config(
    page_title="Forex Trading Dashboard",
    layout="wide"
)


with st.sidebar:

    selected = option_menu(
        "FX Dashboard",
        [
            "Dashboard",
            "Add Trade",
            "Journal",
            "Calendar",
            "Analytics",
            "Edge Analyzer"
        ],
        icons=[
            "bar-chart",
            "plus",
            "journal",
            "calendar",
            "graph-up",
            "cpu"
        ]
    )


if selected == "Dashboard":
    dashboard_page()

elif selected == "Add Trade":
    add_trade_page()

elif selected == "Journal":
    journal_page()

elif selected == "Calendar":
    calendar_page()

elif selected == "Analytics":
    analytics_page()

elif selected == "Edge Analyzer":
    edge_page()
