import streamlit as st
import pandas as pd
from supabase_client import load_trades

st.title("📅 Trading Calendar")

trades = load_trades()

if not trades:
    st.info("No trades yet.")
    st.stop()

df = pd.DataFrame(trades)

df["date"] = pd.to_datetime(df["date"])
df["day"] = df["date"].dt.date

daily_pnl = df.groupby("day")["pnl"].sum()

st.bar_chart(daily_pnl)
