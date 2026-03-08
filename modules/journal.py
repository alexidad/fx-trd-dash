import streamlit as st
import pandas as pd
from modules.supabase_client import load_trades, get_supabase


def journal_page():

    st.title("📓 Trade Journal")

    supabase = get_supabase()

    trades = load_trades()

    if not trades:
        st.info("No trades available.")
        return

    df = pd.DataFrame(trades)

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%b %d")

    st.data_editor(

        df[[
            "id",
            "date",
            "pair",
            "direction",
            "entry",
            "exit_price",
            "lot_size",
            "net_profit",
            "strategy",
            "tag",
            "notes",
            "emotions",
            "rule_violation"
        ]],

        use_container_width=True
    )
