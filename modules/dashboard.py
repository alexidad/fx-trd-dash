import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def dashboard_page():

    st.title("📊 Trading Dashboard")

    trades = load_trades()

    if not trades:
        st.info("No trades recorded yet.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    total_trades = len(df)

    total_profit = df["net_profit"].sum()

    avg_profit = df["net_profit"].mean()

    best_trade = df["net_profit"].max()

    worst_trade = df["net_profit"].min()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", total_trades)
    col2.metric("Total Profit", round(total_profit,2))
    col3.metric("Average Trade", round(avg_profit,2))
    col4.metric("Best Trade", round(best_trade,2))

    st.subheader("Recent Trades")

    st.dataframe(
        df.sort_values("date", ascending=False).head(10),
        use_container_width=True
    )
