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


def calculate_pnl(direction, entry, exit_price, lot):

    if direction == "Buy":
        return (exit_price - entry) * lot * 10000

    else:
        return (entry - exit_price) * lot * 10000


def add_trade_page():

    st.title("Add Trade")

    account = st.session_state.get("selected_account")

    if not account:
        st.warning("Please select an account.")
        return

    col1,col2 = st.columns(2)

    with col1:
        trade_date = st.date_input("Trade Date")

    with col2:
        trade_time = st.time_input("Trade Time")

    col3,col4 = st.columns(2)

    with col3:
        pair = st.text_input("Pair")

    with col4:
        direction = st.selectbox("Direction",["Buy","Sell"])

    col5,col6,col7 = st.columns(3)

    with col5:
        entry = st.number_input("Entry")

    with col6:
        sl = st.number_input("Stop Loss")

    with col7:
        tp = st.number_input("Take Profit")

    col8,col9 = st.columns(2)

    with col8:
        exit_price = st.number_input("Exit Price")

    with col9:
        lot_size = st.number_input("Lot Size")

    col10,col11,col12 = st.columns(3)

    with col10:
        spread = st.number_input("Spread")

    with col11:
        commission = st.number_input("Commission")

    with col12:
        swap = st.number_input("Swap")

    strategy = st.text_input("Strategy")

    tag = st.text_input("Tag")

    chart_url = st.text_input("Chart URL")

    notes = st.text_area("Notes")

    pnl = calculate_pnl(direction,entry,exit_price,lot_size)

    st.metric("Calculated PnL",round(pnl,2))

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

            "net_profit":pnl,

            "chart_url":chart_url,
            "notes":notes
        }

        insert_trade(trade)

        st.success("Trade saved!")
