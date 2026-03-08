import streamlit as st
import pytz
from datetime import datetime

from modules.supabase_client import insert_trade


PH_TIMEZONE = pytz.timezone("Asia/Manila")


def detect_session(hour):

    if 0 <= hour < 7:
        return "Asia"

    if 7 <= hour < 13:
        return "London"

    if 13 <= hour < 16:
        return "Pre-NY"

    if 16 <= hour < 20:
        return "London-NY Overlap"

    return "NY"


def add_trade_page():

    st.title("Add Trade")

    account = st.session_state.get("selected_account")

    if not account:

        st.warning("Please select an account.")
        return

    trade_date = st.date_input("Trade Date")

    trade_time = st.time_input("Trade Time")

    pair = st.text_input("Pair")

    direction = st.selectbox("Direction",["Buy","Sell"])

    strategy = st.text_input("Strategy")

    tag = st.text_input("Tag")

    entry = st.number_input("Entry")

    sl = st.number_input("Stop Loss")

    tp = st.number_input("Take Profit")

    exit_price = st.number_input("Exit Price")

    lot_size = st.number_input("Lot Size")

    spread = st.number_input("Spread")

    commission = st.number_input("Commission")

    swap = st.number_input("Swap")

    net_profit = st.number_input("Net Profit")

    chart_url = st.text_input("Chart URL")

    notes = st.text_area("Notes")

    if st.button("Save Trade"):

        hour = trade_time.hour

        session = detect_session(hour)

        trade = {

            "account":account,
            "date":str(trade_date),
            "time":str(trade_time),

            "pair":pair,
            "direction":direction,
            "session":session,

            "strategy":strategy,
            "tag":tag,

            "entry":entry,
            "sl":sl,
            "tp":tp,
            "exit_price":exit_price,

            "lot_size":lot_size,

            "spread":spread,
            "commission":commission,
            "swap":swap,

            "net_profit":net_profit,

            "chart_url":chart_url,
            "notes":notes
        }

        insert_trade(trade)

        st.success("Trade saved!")
