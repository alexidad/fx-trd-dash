import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades
from modules.metrics_engine import compute_metrics


def dashboard_page():

    st.title("📊 Trading Dashboard")

    trades = load_trades()

    if not trades:
        st.info("No trades recorded yet.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    metrics = compute_metrics(df)

    st.subheader("Trading Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", metrics["total_trades"])
    col2.metric("Win Rate", f'{metrics["win_rate"]}%')
    col3.metric("Profit Factor", metrics["profit_factor"])
    col4.metric("Total Profit", metrics["total_profit"])

    st.divider()

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("Avg Win", metrics["avg_win"])
    col6.metric("Avg Loss", metrics["avg_loss"])
    col7.metric("Best Trade", metrics["best_trade"])
    col8.metric("Worst Trade", metrics["worst_trade"])

    st.divider()

    st.subheader("PnL by Pair")

    pair_perf = df.groupby("pair")["net_profit"].sum()

    st.bar_chart(pair_perf)

    st.subheader("PnL by Weekday")

    df["weekday"] = df["date"].dt.day_name()

    weekday_perf = df.groupby("weekday")["net_profit"].sum()

    st.bar_chart(weekday_perf)

    st.divider()

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
            "net_profit",
            "strategy",
            "tag"
        ]].sort_values("date",ascending=False),

        use_container_width=True
    )
