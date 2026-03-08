import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

PH_TIMEZONE = pytz.timezone("Asia/Manila")

PAIRS = [
    "EURUSD",
    "GBPJPY",
    "USDJPY",
    "AUDUSD",
    "GBPUSD",
    "EURJPY",
    "NZDUSD",
    "XAUUSD"
]

TRADE_COLUMNS = [
    "date",
    "time",
    "pair",
    "direction",
    "session",
    "strategy",
    "tag",
    "entry",
    "sl",
    "tp",
    "exit_price",
    "lot_size",
    "spread",
    "commission",
    "swap",
    "fib_level",
    "pattern",
    "emotion",
    "rule_violation",
    "chart_url",
    "notes",
    "net_profit"
]


def detect_session(hour):

    if hour < 13:
        return "Asia"
    elif hour < 20:
        return "London"
    else:
        return "New York"


def add_trade_page():

    st.title("Add Trade (GMT+8)")

    now = datetime.now(PH_TIMEZONE)

    date = st.date_input("Date", now.date())
    time = st.time_input("Time", now.time())

    session = detect_session(time.hour)

    st.info(f"Detected Session: {session}")

    pair = st.selectbox("Pair", PAIRS)

    direction = st.selectbox("Direction", ["Buy", "Sell"])

    strategy = st.text_input("Strategy")

    tag = st.text_input("Trade Tag")

    entry = st.number_input("Entry Price")

    sl = st.number_input("Stop Loss")

    tp = st.number_input("Take Profit")

    exit_price = st.number_input("Exit Price")

    lot = st.number_input("Lot Size")

    spread = st.number_input("Spread Cost")

    commission = st.number_input("Commission")

    swap = st.number_input("Swap")

    fib = st.selectbox("Fib Level", ["N/A", "50%", "61.8%"])

    pattern = st.text_input("Pattern")

    emotion = st.selectbox(
        "Emotion",
        ["Calm", "Confident", "Fearful", "Frustrated"]
    )

    violation = st.selectbox(
        "Rule Violation",
        ["None", "Early Entry", "Ignored News", "Moved SL", "Overtrading"]
    )

    chart_url = st.text_input("TradingView Chart URL")

    notes = st.text_area("Notes")

    if st.button("Save Trade"):

        net_profit = (exit_price - entry) * lot * 100000

        if direction == "Sell":
            net_profit = (entry - exit_price) * lot * 100000

        new_trade = pd.DataFrame([[
            date,
            time,
            pair,
            direction,
            session,
            strategy,
            tag,
            entry,
            sl,
            tp,
            exit_price,
            lot,
            spread,
            commission,
            swap,
            fib,
            pattern,
            emotion,
            violation,
            chart_url,
            notes,
            net_profit
        ]], columns=TRADE_COLUMNS)

        os.makedirs("accounts", exist_ok=True)

        file = "accounts/default_trades.csv"

        if os.path.exists(file):

            existing = pd.read_csv(file)

            updated = pd.concat([existing, new_trade])

        else:

            updated = new_trade

        updated.to_csv(file, index=False)

        st.success("Trade saved successfully")
