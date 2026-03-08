import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase() -> Client:

    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]

    return create_client(url, key)


def load_trades():

    supabase = get_supabase()

    response = supabase.table("trades").select("*").execute()

    return response.data if response.data else []


def load_accounts():

    supabase = get_supabase()

    response = supabase.table("accounts").select("*").execute()

    return response.data if response.data else []
