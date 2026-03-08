import streamlit as st
from modules.supabase_client import load_accounts


def risk_page():

    st.title("Risk Calculator")

    accounts = load_accounts()

    account_names = [a["account_name"] for a in accounts]

    selected = st.selectbox("Account",account_names)

    account = next(a for a in accounts if a["account_name"] == selected)

    balance = account["starting_balance"]

    st.metric("Account Balance",balance)

    pair = st.text_input("Pair")

    risk_percent = st.number_input("Risk %",value=1.0)

    stop_loss = st.number_input("Stop Loss (pips)")

    if "JPY" in pair.upper():
        pip_value = 9.13
    else:
        pip_value = 10

    risk_amount = balance * (risk_percent/100)

    if stop_loss > 0:

        lot_size = risk_amount / (stop_loss * pip_value)

        st.success(f"Recommended Lot Size: {round(lot_size,2)}")
