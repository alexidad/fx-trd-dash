import streamlit as st
from datetime import datetime
import pytz
from modules.supabase_client import get_supabase

PH_TIMEZONE = pytz.timezone("Asia/Manila")

PAIRS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF",
    "NZDUSD",
    "EURJPY",
    "GBPJPY",
]

SETUPS = [
    "BRC + Fib 50",
    "BRC + Fib 61.8",
    "Support / Resistance",
    "Trend Continuation",
    "Breakout",
    "Other",
]


def add_trade_page():

    st.title("➕ Add Trade")

    col1, col2 = st.columns(2)

    with col1:
        pair = st.selectbox("Pair", PAIRS)

    with col2:
        setup = st.selectbox("Setup", SETUPS)

    result = st.selectbox(
        "Result",
        ["Win", "Loss", "Breakeven"]
    )

    r_multiple = st.number_input(
        "R Multiple",
        value=0.0,
        step=0.25,
        help="Example: +1.5R, -1R"
    )

    notes = st.text_area(
        "Trade Notes",
        placeholder="Why did you take this trade?"
    )

    screenshot = st.file_uploader(
        "Upload Chart Screenshot (optional)",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Save Trade"):

        supabase = get_supabase()

        trade_data = {
            "pair": pair,
            "setup": setup,
            "result": result,
            "pnl": r_multiple,
            "notes": notes,
            "date": datetime.now(PH_TIMEZONE).isoformat()
        }

        supabase.table("trades").insert(trade_data).execute()

        st.success("Trade saved successfully!")
