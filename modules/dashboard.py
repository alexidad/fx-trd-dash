import streamlit as st
import pandas as pd
import plotly.express as px
import os

ACCOUNTS_FILE = "accounts.csv"
ACCOUNTS_FOLDER = "accounts"

def dashboard_page():

    st.title("Dashboard")

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

    if len(trades) == 0:
        st.warning("No trades yet")
        return

    total_profit = trades["net_profit"].sum()
    win_rate = (trades["net_profit"] > 0).mean() * 100
    trades_count = len(trades)

    equity = trades["net_profit"].cumsum()
    drawdown = equity.min()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Net Profit", f"${total_profit:,.2f}")
    c2.metric("Win Rate", f"{win_rate:.1f}%")
    c3.metric("Trades", trades_count)
    c4.metric("Drawdown", f"${drawdown:,.2f}")

    st.subheader("Equity Curve")

    fig = px.line(equity)

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Session Heatmap")

    session_perf = trades.groupby(
        ["pair","session"]
    )["net_profit"].sum().reset_index()

    fig = px.density_heatmap(
        session_perf,
        x="pair",
        y="session",
        z="net_profit",
        color_continuous_scale="RdYlGn"
    )

    st.plotly_chart(fig, use_container_width=True)