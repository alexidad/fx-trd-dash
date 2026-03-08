import streamlit as st
from streamlit_option_menu import option_menu

from modules.dashboard import dashboard_page
from modules.add_trade import add_trade_page
from modules.journal import journal_page
from modules.edge_analyzer import edge_page
from modules.accounts_page import accounts_page
from modules.risk_tools import risk_page

from modules.supabase_client import load_accounts


st.set_page_config(
    page_title="Forex Trading Dashboard",
    layout="wide"
)


# Load accounts from Supabase
accounts = load_accounts()

account_names = [a["account_name"] for a in accounts] if accounts else []


# SIDEBAR
with st.sidebar:

    st.title("FX Dashboard")

    if account_names:

        selected_account = st.selectbox(
            "Select Account",
            account_names
        )

        # Store globally for other modules
        st.session_state["selected_account"] = selected_account

    else:

        st.warning("No accounts created")

    selected = option_menu(
        "Menu",
        [
            "Dashboard",
            "Add Trade",
            "Journal",
            "Risk Tools",
            "Edge Analyzer",
            "Accounts"
        ],
        icons=[
            "bar-chart",
            "plus-circle",
            "journal",
            "calculator",
            "cpu",
            "wallet"
        ],
        default_index=0
    )


# PAGE ROUTING

if selected == "Dashboard":

    dashboard_page()

elif selected == "Add Trade":

    add_trade_page()

elif selected == "Journal":

    journal_page()

elif selected == "Risk Tools":

    risk_page()

elif selected == "Edge Analyzer":

    edge_page()

elif selected == "Accounts":

    accounts_page()
