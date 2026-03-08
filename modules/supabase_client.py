import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase():

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    return create_client(url, key)


def load_trades():

    supabase = get_supabase()

    response = supabase.table("trades").select("*").execute()

    if response.data:
        return response.data

    return []


def insert_trade(trade):

    supabase = get_supabase()

    supabase.table("trades").insert(trade).execute()


def update_trade(trade_id, updates):

    supabase = get_supabase()

    supabase.table("trades").update(updates).eq("id", trade_id).execute()


def delete_trade(trade_id):

    supabase = get_supabase()

    supabase.table("trades").delete().eq("id", trade_id).execute()
