import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Forex Trading Dashboard", layout="wide")

DATA_FILE = "trades.csv"

# ---------------------------
# Load or Create Trade Data
# ---------------------------

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "date","time","pair","direction","session",
        "entry","sl","tp","lot_size",
        "result","R","fib_level","pattern",
        "emotion","rule_violation","notes"
    ])

# ---------------------------
# Sidebar Navigation
# ---------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Add Trade",
        "Trade Journal",
        "Risk Tools",
        "Prop Firm Tracker"
    ]
)

# ---------------------------
# Dashboard
# ---------------------------

if page == "Dashboard":

    st.title("Forex Trading Dashboard")

    if len(df) == 0:
        st.warning("No trades logged yet.")
        st.stop()

    total_trades = len(df)
    win_rate = (df["result"] > 0).mean() * 100
    total_profit = df["result"].sum()

    avg_win = df[df["result"] > 0]["result"].mean()
    avg_loss = df[df["result"] < 0]["result"].mean()

    expectancy = (win_rate/100 * avg_win) + ((1-win_rate/100) * avg_loss)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Trades", total_trades)
    col2.metric("Win Rate", f"{win_rate:.1f}%")
    col3.metric("Total Profit", f"${total_profit:.2f}")
    col4.metric("Expectancy", f"{expectancy:.2f}")

    # Equity curve
    df["equity"] = df["result"].cumsum()

    fig = px.line(df, y="equity", title="Equity Curve")
    st.plotly_chart(fig, use_container_width=True)

    # Pair performance
    st.subheader("Pair Performance")

    pair_perf = df.groupby("pair")["result"].sum().reset_index()

    fig = px.bar(pair_perf, x="pair", y="result", title="Profit by Pair")
    st.plotly_chart(fig, use_container_width=True)

    # Session performance
    st.subheader("Session Performance")

    session_perf = df.groupby("session")["result"].sum().reset_index()

    fig = px.bar(session_perf, x="session", y="result")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Add Trade
# ---------------------------

elif page == "Add Trade":

    st.title("Add Trade")

    with st.form("trade_form"):

        date = st.date_input("Date")
        time = st.time_input("Time")

        pair = st.selectbox(
            "Pair",
            ["USDJPY","AUDUSD","EURJPY","NZDUSD","EURUSD","GBPUSD","GBPJPY"]
        )

        direction = st.selectbox("Direction",["Buy","Sell"])

        session = st.selectbox(
            "Session",
            ["Asia","London","NY Overlap"]
        )

        entry = st.number_input("Entry Price")
        sl = st.number_input("Stop Loss")
        tp = st.number_input("Take Profit")

        lot_size = st.number_input("Lot Size")

        result = st.number_input("Result ($)")

        R = st.number_input("R Multiple")

        fib_level = st.selectbox(
            "Fib Level",
            ["50%","61.8%"]
        )

        pattern = st.selectbox(
            "Pattern",
            ["Engulfing","Hammer","Morning Star","Evening Star"]
        )

        emotion = st.selectbox(
            "Emotion",
            ["Calm","Confident","Fearful","Frustrated"]
        )

        rule_violation = st.selectbox(
            "Rule Violation",
            ["None","Early Entry","Ignored News","Moved SL","Overtrading"]
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Add Trade")

        if submitted:

            new_trade = pd.DataFrame([[
                date,time,pair,direction,session,
                entry,sl,tp,lot_size,
                result,R,fib_level,pattern,
                emotion,rule_violation,notes
            ]], columns=df.columns)

            df = pd.concat([df,new_trade],ignore_index=True)

            df.to_csv(DATA_FILE,index=False)

            st.success("Trade added successfully!")

# ---------------------------
# Trade Journal
# ---------------------------

elif page == "Trade Journal":

    st.title("Trade Journal")

    st.dataframe(df, use_container_width=True)

# ---------------------------
# Risk Tools
# ---------------------------

elif page == "Risk Tools":

    st.title("Risk Tools")

    st.subheader("Auto Lot Size Calculator")

    account_size = st.number_input("Account Size", value=6000)

    risk_percent = st.number_input("Risk %", value=1.0)

    sl_pips = st.number_input("Stop Loss (pips)", value=30)

    pair_type = st.selectbox("Pair Type",["USD Pair","JPY Pair"])

    risk_amount = account_size * (risk_percent/100)

    pip_value = 10 if pair_type == "USD Pair" else 6.67

    lot_size = risk_amount / (sl_pips * pip_value)

    st.write(f"Risk Amount: ${risk_amount:.2f}")
    st.write(f"Lot Size: {lot_size:.2f}")

    st.subheader("Trade Setup Validator")

    trend = st.checkbox("Trend aligned")
    fib = st.checkbox("Fib level valid")
    rr = st.checkbox("RR ≥ 1.5")
    news = st.checkbox("No major news")

    if trend and fib and rr and news:
        st.success("Valid Trade")
    else:
        st.error("Do Not Trade")

# ---------------------------
# Prop Firm Tracker
# ---------------------------

elif page == "Prop Firm Tracker":

    st.title("Prop Firm Tracker")

    starting_balance = st.number_input("Starting Balance", value=6000)

    phase_target = st.number_input("Phase Target", value=6480)

    daily_loss_limit = st.number_input("Daily Loss Limit", value=300)

    max_loss_limit = st.number_input("Max Loss Limit", value=600)

    current_balance = starting_balance + df["result"].sum()

    drawdown = starting_balance - current_balance

    progress = current_balance - starting_balance

    col1,col2,col3 = st.columns(3)

    col1.metric("Current Balance",f"${current_balance:.2f}")
    col2.metric("Progress",f"${progress:.2f}")
    col3.metric("Drawdown",f"${drawdown:.2f}")

    st.progress(current_balance/phase_target)