import streamlit as st
import pandas as pd
import plotly.express as px
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def analytics_page():

    st.title("Analytics")

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

    st.subheader("Filters")

    pair = st.selectbox(
        "Pair",
        ["All"] + sorted(trades["pair"].dropna().unique().tolist())
    )

    session = st.selectbox(
        "Session",
        ["All"] + sorted(trades["session"].dropna().unique().tolist())
    )

    tag = st.selectbox(
        "Tag",
        ["All"] + sorted(trades["tag"].dropna().unique().tolist())
    )

    if pair != "All":
        trades = trades[trades["pair"] == pair]

    if session != "All":
        trades = trades[trades["session"] == session]

    if tag != "All":
        trades = trades[trades["tag"] == tag]

    st.subheader("Pair Profitability")

    pair_perf = trades.groupby("pair")["net_profit"].sum().reset_index()

    fig = px.bar(
        pair_perf,
        x="pair",
        y="net_profit",
        color="net_profit",
        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Session Performance")

    session_perf = trades.groupby("session")["net_profit"].sum().reset_index()

    fig = px.bar(
        session_perf,
        x="session",
        y="net_profit",
        color="net_profit"
    )

    st.plotly_chart(fig, use_container_width=True)