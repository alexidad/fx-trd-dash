import streamlit as st
import pandas as pd
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def edge_page():

    st.title("Edge Analyzer")

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

    st.subheader("Best Setups")

    combos = trades.groupby(
        ["pair","session","strategy","tag"]
    )["net_profit"].agg(["sum","count"])

    combos = combos.sort_values("sum",ascending=False)

    st.dataframe(combos.head(10))

    st.subheader("Worst Setups")

    st.dataframe(combos.tail(10))