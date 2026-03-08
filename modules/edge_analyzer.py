import streamlit as st
import pandas as pd
from supabase_client import load_trades

st.title("🧠 Edge Analyzer")

trades = load_trades()

if not trades:
    st.info("No trades yet.")
    st.stop()

df = pd.DataFrame(trades)

setup_perf = df.groupby("setup")["pnl"].agg(["count", "sum", "mean"])

st.subheader("Setup Performance")

st.dataframe(setup_perf)
