import streamlit as st
from datetime import datetime
import pytz
from modules.supabase_client import get_supabase

PH_TIMEZONE = pytz.timezone("Asia/Manila")


def add_trade_page():

    st.title("➕ Add Trade")

    pair = st.text_input("Pair")
    setup = st.text_input("Setup")

    result = st.selectbox(
        "Result",
        ["Win", "Loss", "Breakeven"]
    )

    pnl = st.number_input("PnL", step=0.1)

    if st.button("Save Trade"):

        supabase = get_supabase()

        trade_data = {
            "pair": pair,
            "setup": setup,
            "result": result,
            "pnl": pnl,
            "date": datetime.now(PH_TIMEZONE).isoformat()
        }

        supabase.table("trades").insert(trade_data).execute()

        st.success("Trade saved!")
