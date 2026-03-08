import streamlit as st
import pandas as pd
import plotly.express as px
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def calendar_page():

    st.title("Trading Calendar")

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

    trades["date"] = pd.to_datetime(trades["date"])

    daily = trades.groupby("date").agg(
        profit=("net_profit","sum"),
        trades=("net_profit","count")
    ).reset_index()

    daily["month"] = daily["date"].dt.month
    daily["day"] = daily["date"].dt.day

    st.subheader("Daily Performance Heatmap")

    fig = px.density_heatmap(
        daily,
        x="day",
        y="month",
        z="profit",
        color_continuous_scale="RdYlGn",
        nbinsx=31,
        nbinsy=12
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Daily Summary")

    st.dataframe(daily)