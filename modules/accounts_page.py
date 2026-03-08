import streamlit as st
import pandas as pd

ACCOUNTS_FILE = "accounts.csv"

def accounts_page():

    st.title("Manage Accounts")

    accounts = pd.read_csv(ACCOUNTS_FILE)

    st.subheader("Existing Accounts")
    st.dataframe(accounts)

    st.subheader("Create New Account")

    name = st.text_input("Account Name")

    acc_type = st.selectbox(
        "Account Type",
        ["propfirm","personal","backtest"]
    )

    balance = st.number_input("Starting Balance")

    risk = st.number_input("Risk % per trade")

    daily = st.number_input("Daily Loss Limit")

    drawdown = st.number_input("Max Drawdown")

    if st.button("Create Account"):

        new = pd.DataFrame([[
            name,acc_type,balance,risk,daily,drawdown
        ]],columns=[
            "account_name","account_type",
            "starting_balance","risk_per_trade",
            "daily_loss_limit","max_drawdown"
        ])

        accounts = pd.concat([accounts,new])

        accounts.to_csv(ACCOUNTS_FILE,index=False)

        st.success("Account created")

    st.subheader("Delete Account")

    delete_acc = st.selectbox(
        "Select account to delete",
        accounts["account_name"]
    )

    if st.button("Delete"):

        accounts = accounts[accounts["account_name"] != delete_acc]

        accounts.to_csv(ACCOUNTS_FILE,index=False)

        st.success("Account deleted")