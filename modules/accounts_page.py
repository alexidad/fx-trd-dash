import streamlit as st
import pandas as pd
from modules.supabase_client import get_supabase


def accounts_page():

    st.title("Manage Accounts")

    supabase = get_supabase()

    response = supabase.table("accounts").select("*").execute()

    accounts = pd.DataFrame(response.data)

    if not accounts.empty:

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

        supabase.table("accounts").insert({

            "account_name": name,
            "account_type": acc_type,
            "starting_balance": balance,
            "risk_per_trade": risk,
            "daily_loss_limit": daily,
            "max_drawdown": drawdown

        }).execute()

        st.success("Account created")

    st.subheader("Delete Account")

    if not accounts.empty:

        delete_acc = st.selectbox(
            "Select account to delete",
            accounts["account_name"]
        )

        if st.button("Delete"):

            supabase.table("accounts") \
                .delete() \
                .eq("account_name", delete_acc) \
                .execute()

            st.success("Account deleted")
