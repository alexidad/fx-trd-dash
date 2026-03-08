import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def calendar_page():

    st.title("📅 Trading Calendar")

    trades = load_trades()

    if not trades:
        st.info("No trades yet.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    df["day"] = df["date"].dt.date

    daily = df.groupby("day")["pnl"].sum()

    st.bar_chart(daily)
