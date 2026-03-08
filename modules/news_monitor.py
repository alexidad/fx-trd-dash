import requests
import streamlit as st
import xml.etree.ElementTree as ET

URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"

def news_banner():

    try:

        data = requests.get(URL).content

        root = ET.fromstring(data)

        for item in root.findall(".//event"):

            impact = item.find("impact").text

            if impact == "High":

                title = item.find("title").text

                st.warning(f"⚠ High Impact News: {title}")

                break

    except:

        pass