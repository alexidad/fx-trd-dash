import streamlit as st
import pandas as pd
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def mt5_import_page():

    st.title("Import MT5 Trades")

    accounts = pd.read_csv(ACCOUNTS_FILE)

    account = st.sidebar.selectbox(
        "Account",
        accounts["account_name"]
    )

    file = st.file_uploader("Upload MT5 CSV")

    if file:

        mt5 = pd.read_csv(file)

        st.write("Preview")

        st.dataframe(mt5.head())

        if st.button("Import Trades"):

            trades = pd.DataFrame()

            trades["date"] = mt5["Time"]
            trades["pair"] = mt5["Symbol"]
            trades["direction"] = mt5["Type"]
            trades["lot_size"] = mt5["Volume"]

            trades["entry"] = mt5["Price"]

            trades["sl"] = mt5["S/L"]
            trades["tp"] = mt5["T/P"]

            trades["net_profit"] = mt5["Profit"]

            trades["commission"] = mt5["Commission"]
            trades["swap"] = mt5["Swap"]

            trades["strategy"] = ""
            trades["tag"] = ""
            trades["pattern"] = ""
            trades["emotion"] = ""
            trades["rule_violation"] = ""
            trades["fib_level"] = ""
            trades["chart_url"] = ""
            trades["notes"] = ""

            save = f"{ACCOUNTS_FOLDER}/{account.replace(' ','_').lower()}_trades.csv"

            if os.path.exists(save):

                old = pd.read_csv(save)

                trades = pd.concat([old,trades])

            trades.to_csv(save,index=False)

            st.success("Trades imported")