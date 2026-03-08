import streamlit as st


def risk_page():

    st.title("⚠️ Risk Tools")

    balance = st.number_input("Account Balance")

    risk_percent = st.number_input("Risk % per trade",value=1.0)

    stop_loss = st.number_input("Stop Loss (pips)")

    pip_value = st.number_input("Pip Value",value=10.0)

    if stop_loss > 0:

        risk_amount = balance * (risk_percent/100)

        lot_size = risk_amount / (stop_loss * pip_value)

        st.success(f"Recommended Lot Size: {round(lot_size,2)}")
