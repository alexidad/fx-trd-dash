import streamlit as st
import pandas as pd

ACCOUNTS_FILE = "accounts.csv"

def risk_page():

    st.title("Risk Tools")

    accounts = pd.read_csv(ACCOUNTS_FILE)

    account = st.sidebar.selectbox(
        "Account",
        accounts["account_name"]
    )

    acc = accounts[accounts["account_name"] == account].iloc[0]

    balance = acc["starting_balance"]
    risk_percent = acc["risk_per_trade"]

    st.subheader("Lot Size Calculator")

    sl = st.number_input("Stop Loss (pips)", 20)

    pair_type = st.selectbox(
        "Pair Type",
        ["USD pair","JPY pair"]
    )

    pip_value = 10 if pair_type == "USD pair" else 6.67

    risk_amount = balance * (risk_percent / 100)

    lot = risk_amount / (sl * pip_value)

    st.markdown(f"## Risk Amount: ${risk_amount:,.2f}")
    st.markdown(f"# Recommended Lot Size: {lot:.2f}")

    st.subheader("Lot Size Table")

    table = []

    for p in [10,15,20,25,30,40,50]:

        table.append({
            "SL (pips)": p,
            "Lot Size": round(risk_amount / (p * pip_value),2)
        })

    st.dataframe(pd.DataFrame(table))