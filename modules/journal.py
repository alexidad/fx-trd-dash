import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades


def journal_page():

    st.title("Trade Journal")

    trades = load_trades()

    if not trades:
        st.info("No trades available.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%b %d")

    display_columns = [

        "date",
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
        "net_profit",
        "notes"

    ]

    st.data_editor(

        df[display_columns],

        use_container_width=True
    )
