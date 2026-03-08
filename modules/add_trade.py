import streamlit as st
from datetime import datetime, time
import pytz
from modules.supabase_client import get_supabase

PH_TIMEZONE = pytz.timezone("Asia/Manila")

PAIRS = [
    "EURUSD","GBPUSD","USDJPY","AUDUSD",
    "USDCAD","USDCHF","NZDUSD","EURJPY","GBPJPY"
]

DIRECTIONS = ["Buy", "Sell"]

STRATEGIES = [
    "BRC",
    "Fibonacci",
    "Support / Resistance",
    "Breakout",
    "Trend Continuation"
]


def detect_session(trade_time):

    hour = trade_time.hour

    if 0 <= hour < 9:
        return "Tokyo"

    elif 9 <= hour < 16:
        return "London"

    elif 16 <= hour < 20:
        return "Pre-NY"

    else:
        return "London-NY Overlap"



def add_trade_page():

    st.title("➕ Add Trade")

    supabase = get_supabase()

    st.subheader("Trade Information")

    col1, col2 = st.columns(2)

    with col1:

        account = st.text_input("Account")

        pair = st.selectbox("Pair", PAIRS)

        direction = st.selectbox("Direction", DIRECTIONS)

        strategy = st.selectbox("Strategy", STRATEGIES)

        tag = st.text_input("Tag")

    with col2:

        trade_date = st.date_input("Trade Date")

        trade_time = st.time_input("Trade Time")

        session = detect_session(trade_time)

        st.write(f"Detected Session: **{session}**")


    st.divider()


    st.subheader("Price Data")

    col3, col4 = st.columns(2)

    with col3:

        entry = st.number_input("Entry Price", value=0.0)

        sl = st.number_input("Stop Loss", value=0.0)

        tp = st.number_input("Take Profit", value=0.0)

        exit_price = st.number_input("Exit Price", value=0.0)

    with col4:

        lot_size = st.number_input("Lot Size", value=0.01)

        spread = st.number_input("Spread", value=0.0)

        commission = st.number_input("Commission", value=0.0)

        swap = st.number_input("Swap", value=0.0)

        net_profit = st.number_input("Net Profit", value=0.0)


    st.divider()

    notes = st.text_area("Trade Notes")

    chart_url = st.text_input("Chart Screenshot URL (optional)")


    if st.button("Save Trade"):

        trade_data = {

            "account": account,
            "date": trade_date.isoformat(),
            "time": trade_time.strftime("%H:%M:%S"),
            "pair": pair,
            "direction": direction,
            "session": session,
            "strategy": strategy,
            "tag": tag,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "exit_price": exit_price,
            "lot_size": lot_size,
            "spread": spread,
            "commission": commission,
            "swap": swap,
            "net_profit": net_profit,
            "chart_url": chart_url,
            "notes": notes
        }

        try:

            supabase.table("trades").insert(trade_data).execute()

            st.success("Trade saved successfully!")

        except Exception as e:

            st.error("Error saving trade")
            st.write(e)
