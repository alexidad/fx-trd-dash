import streamlit as st
import pandas as pd
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def journal_page():

    st.title("Trade Journal")

    accounts = pd.read_csv(ACCOUNTS_FILE)

    account = st.sidebar.selectbox(
        "Account",
        accounts["account_name"]
    )

    file = f"{ACCOUNTS_FOLDER}/{account.replace(' ','_').lower()}_trades.csv"

    if not os.path.exists(file):

        st.warning("No trades yet")
        return

    trades = pd.read_csv(file)

    cols = st.columns(3)

    for i,trade in trades.iterrows():

        with cols[i % 3]:

            profit = trade["net_profit"]

            color = "green" if profit >= 0 else "red"

            st.markdown(
                f"""
                ### {trade['pair']}
                **{trade['direction']}**

                Profit: :{color}[${profit:,.2f}]

                Session: {trade['session']}

                Strategy: {trade['strategy']}

                Tag: {trade['tag']}
                """
            )

            if trade["chart_url"]:

                st.link_button("View Chart", trade["chart_url"])

            if trade["notes"]:

                st.caption(trade["notes"])

            st.divider()