import os
import time
import streamlit as st
from dotenv import load_dotenv
from src.scraper import scrape_user_data
from src.persona_ai import generate_persona

load_dotenv()

st.set_page_config(page_title="Reddit Persona Generator", layout="centered")

st.title("🔍 Reddit Persona Generator")
st.markdown("""
Enter a Reddit **username**, and we'll scrape their recent comments and text-only posts to build a psychological and behavioral **persona profile** using AI.
""")

username = st.text_input("Reddit Username (without /u/)", "kojied")

if st.button("Find Out"):
    with st.spinner("Scraping Reddit and analyzing personality with AI..."):
        comments, posts = scrape_user_data(username)
        if not comments and not posts:
            st.error("Couldn't fetch enough content to build a persona.")
        else:
            result = generate_persona(username, comments, posts)

            st.success("Persona generated!")
            st.download_button(
                label="⬇️ Download Persona as .txt",
                data=result,
                file_name=f"{username}_persona.txt",
                mime="text/plain"
            )