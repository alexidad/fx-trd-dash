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

    st.subheader("Strategy Performance")

    strategy_perf = df.groupby("strategy")["net_profit"].agg(
        trades="count",
        total_profit="sum",
        avg_profit="mean"
    )

    st.dataframe(strategy_perf, use_container_width=True)
