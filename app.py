import streamlit as st
from streamlit_option_menu import option_menu

from modules.dashboard import dashboard_page
from modules.add_trade import add_trade_page
from modules.journal import journal_page
from modules.calendar_view import calendar_page
from modules.analytics import analytics_page
from modules.risk_tools import risk_page
from modules.accounts_page import accounts_page
from modules.edge_analyzer import edge_page
from modules.news_monitor import news_banner

st.set_page_config(layout="wide", page_title="Trading Dashboard")

# News banner
news_banner()

# Sidebar navigation
with st.sidebar:

    st.title("Trading Dashboard")

    page = option_menu(
        "Navigation",
        [
            "Dashboard",
            "Calendar",
            "Journal",
            "Add Trade",
            "Analytics",
            "Edge Analyzer",
            "Risk Tools",
            "Accounts"
        ],
        icons=[
            "bar-chart",
            "calendar",
            "journal",
            "plus-circle",
            "graph-up",
            "search",
            "calculator",
            "gear"
        ],
        menu_icon="cast",
        default_index=0
    )

# Page routing
if page == "Dashboard":
    dashboard_page()

elif page == "Calendar":
    calendar_page()

elif page == "Journal":
    journal_page()

elif page == "Add Trade":
    add_trade_page()

elif page == "Analytics":
    analytics_page()

elif page == "Edge Analyzer":
    edge_page()

elif page == "Risk Tools":
    risk_page()

elif page == "Accounts":
    accounts_page()
