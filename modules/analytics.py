import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def analytics_page():

    st.title("📈 Analytics")

    trades = load_trades()

    if not trades:
        st.info("No trades recorded.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M")

    st.subheader("Monthly Profit")

    monthly = df.groupby("month")["net_profit"].sum()

    st.bar_chart(monthly)

    st.subheader("Profit by Pair")

    pair_perf = df.groupby("pair")["net_profit"].sum()

    st.bar_chart(pair_perf)
