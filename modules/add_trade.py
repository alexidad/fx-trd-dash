import streamlit as st
from datetime import datetime
import pytz
from modules.supabase_client import get_supabase


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

    if "active_account" not in st.session_state:

        st.warning("Please create or select an account first.")
        return

    account = st.session_state["active_account"]

    st.write(f"Account: **{account}**")

    supabase = get_supabase()

    col1, col2 = st.columns(2)

    with col1:

        pair = st.text_input("Pair")

        direction = st.selectbox(
            "Direction",
            ["Buy", "Sell"]
        )

        strategy = st.text_input("Strategy")

        tag = st.text_input("Tag")

    with col2:

        trade_date = st.date_input("Trade Date")

        trade_time = st.time_input(
            "Trade Time (AM/PM)"
        )

        session = detect_session(trade_time)

        st.write(f"Detected Session: **{session}**")

    st.divider()

    col3, col4 = st.columns(2)

    with col3:

        entry = st.number_input("Entry Price")

        sl = st.number_input("Stop Loss")

        tp = st.number_input("Take Profit")

        exit_price = st.number_input("Exit Price")

    with col4:

        lot_size = st.number_input("Lot Size")

        spread = st.number_input("Spread")

        commission = st.number_input("Commission")

        swap = st.number_input("Swap")

        net_profit = st.number_input("Net Profit")

    st.divider()

    chart_url = st.text_input("Chart URL")

    notes = st.text_area("Notes")

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

        supabase.table("trades").insert(trade_data).execute()

        st.success("Trade saved!")
