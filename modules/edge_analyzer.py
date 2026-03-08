import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def edge_page():

    st.title("🧠 Edge Analyzer")

    trades = load_trades()

    if not trades:
        st.info("No trades recorded.")
        return

    df = pd.DataFrame(trades)

    st.subheader("Performance by Strategy")

    strategy_perf = df.groupby("strategy")["net_profit"].sum()

    st.bar_chart(strategy_perf)

    st.subheader("Performance by Pair")

    pair_perf = df.groupby("pair")["net_profit"].sum()

    st.bar_chart(pair_perf)

    st.subheader("Performance by Session")

    session_perf = df.groupby("session")["net_profit"].sum()

    st.bar_chart(session_perf)
