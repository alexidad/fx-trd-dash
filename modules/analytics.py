import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def analytics_page():

    st.title("📈 Trade Analytics")

    trades = load_trades()

    if not trades:
        st.info("No trades yet.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.to_period("M")

    st.subheader("Monthly Performance")

    monthly = df.groupby("month")["pnl"].sum()

    st.bar_chart(monthly)

    st.subheader("Performance by Pair")

    pair_perf = df.groupby("pair")["pnl"].sum()

    st.bar_chart(pair_perf)
