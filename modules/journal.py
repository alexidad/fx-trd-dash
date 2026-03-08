import streamlit as st
import pandas as pd
from supabase_client import load_trades

st.title("📓 Trade Journal")

trades = load_trades()

if not trades:
    st.info("No trades recorded.")
    st.stop()

df = pd.DataFrame(trades)
df["date"] = pd.to_datetime(df["date"])

pairs = sorted(df["pair"].unique())

pair_filter = st.selectbox("Filter by Pair", ["All"] + pairs)

if pair_filter != "All":
    df = df[df["pair"] == pair_filter]

st.dataframe(df.sort_values("date", ascending=False))
