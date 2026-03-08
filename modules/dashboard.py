import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def dashboard_page():

    st.title("📊 Trading Dashboard")

    trades = load_trades()

    if not trades:
        st.info("No trades recorded yet.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"])

    total_trades = len(df)
    wins = len(df[df["result"] == "Win"])
    losses = len(df[df["result"] == "Loss"])

    winrate = (wins / total_trades) * 100 if total_trades else 0
    total_pnl = df["pnl"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trades", total_trades)
    col2.metric("Win Rate", f"{winrate:.2f}%")
    col3.metric("Wins", wins)
    col4.metric("Total PnL", f"{total_pnl:.2f}")

    st.subheader("Recent Trades")

    st.dataframe(
        df.sort_values("date", ascending=False).head(10),
        use_container_width=True
    )
