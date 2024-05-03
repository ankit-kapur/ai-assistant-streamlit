import validators
import streamlit as st

def validate_url(website_url):
    if (website_url == None or website_url == ""):
        st.warning("⚠️ URL is empty")
        return False
    elif not validators.url(website_url):
        st.error("⚠️ Invalid URL")
        return False
    else:
        return True
