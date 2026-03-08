import streamlit as st
import pandas as pd
from supabase_client import load_trades

st.title("📈 Trade Analytics")

trades = load_trades()

if not trades:
    st.info("No trades available.")
    st.stop()

df = pd.DataFrame(trades)

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly_pnl = df.groupby("month")["pnl"].sum()

st.subheader("Monthly Performance")

st.bar_chart(monthly_pnl)

st.subheader("Pair Performance")

pair_perf = df.groupby("pair")["pnl"].sum()

st.bar_chart(pair_perf)
