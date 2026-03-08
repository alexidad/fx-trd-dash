import streamlit as st
import pandas as pd

from modules.supabase_client import load_trades
from modules.metrics_engine import compute_metrics


def dashboard_page():

    st.title("Trading Dashboard")

    account = st.session_state.get("selected_account")

    trades = load_trades()

    if not trades:

        st.info("No trades yet.")
        return

    df = pd.DataFrame(trades)

    if account:
        df = df[df["account"] == account]

    if df.empty:

        st.info("No trades for this account.")
        return

    df["date"] = pd.to_datetime(df["date"])

    metrics = compute_metrics(df)

    st.subheader("Trading Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Trades",metrics["total_trades"])
    c2.metric("Win Rate",f'{metrics["win_rate"]}%')
    c3.metric("Profit Factor",metrics["profit_factor"])
    c4.metric("Total Profit",metrics["total_profit"])

    st.divider()

    c5,c6,c7,c8 = st.columns(4)

    c5.metric("Avg Win",metrics["avg_win"])
    c6.metric("Avg Loss",metrics["avg_loss"])
    c7.metric("Best Trade",metrics["best_trade"])
    c8.metric("Worst Trade",metrics["worst_trade"])

    st.divider()

    st.subheader("PnL by Pair")

    pair_perf = df.groupby("pair")["net_profit"].sum()

    st.bar_chart(pair_perf)

    st.subheader("Recent Trades")

    df["date"] = df["date"].dt.strftime("%b %d")

    st.dataframe(

        df[[
        "date",
        "pair",
        "direction",
        "entry",
        "sl",
        "tp",
        "exit_price",
        "lot_size",
        "net_profit"
        ]].sort_values("date",ascending=False),

        use_container_width=True
    )
