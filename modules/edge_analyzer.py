import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def edge_page():

    st.title("🧠 Edge Analyzer")

    trades = load_trades()

    if not trades:
        st.info("No trades yet.")
        return

    df = pd.DataFrame(trades)

    st.subheader("Setup Performance")

    setup_perf = df.groupby("setup")["pnl"].agg(["count", "sum", "mean"])

    st.dataframe(setup_perf, use_container_width=True)
