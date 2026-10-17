import json
import re
from urllib.parse import quote

import streamlit.components.v1 as components
from google import genai
from google.genai import types
import streamlit as st
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT

NutriScan_API_Key = st.secrets["NutriScan_API_Key"]


@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=NutriScan_API_Key)

gemini_client = get_gemini_client()

MODEL_NAME = "gemini-3.5-flash-lite"


def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong : {error}"

def trim_for_link(text, limit=1200):
    if len(text) <= limit:
        return text
    cut = text[:limit]
    return cut.rsplit("\n", 1)[0] + "\n…(full summary in NutriScan)"

#step 1: onboarding (name + WhatsApp number)

if 'onboarded' not in st.session_state:
    st.title("NutriScan 🍱")
    st.caption("Snap it. Track it. Get the result on WhatsApp.")
    st.caption("💡 Tip: upload a meal photo under 1 MB for a faster reply.")

    with st.form("onboarding_form"):
        name = st.text_input("Your name")
        whatsapp_number = st.text_input("Your WhatsApp number (with country code, e.g. 919876543210)")
        submitted = st.form_submit_button("Let's go 👉")

    if submitted:
        digits = re.sub(r"\D", "", whatsapp_number)
        if not name.strip() or len(digits) < 10:
            st.warning("Please enter your name and a valid WhatsApp number with country code.")
        else:
            st.session_state.name = name.strip()
            st.session_state.whatsapp_number = digits
            #activate my ai
            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            st.session_state.messages = []
            st.session_state.onboarded = True
            st.rerun()
    st.stop()

#Create a chat interface

header_col, button_col = st.columns([5, 2], vertical_alignment="center")

with header_col:
    st.title("NutriScan 🍱")

with button_col:
    if st.button("📤 Send to WhatsApp", use_container_width=True):
        if len(st.session_state.messages) <= 1:
            st.warning("Chat about at least one meal first.")
        else:
            with st.spinner("Summarizing your day..."):
                summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
            if summary.startswith("Sorry, something went wrong"):
                st.error(summary)
            else:
                st.session_state.summary = summary
                st.session_state.wa_link = (
                    f"https://wa.me/{st.session_state.whatsapp_number}?text={quote(trim_for_link(summary))}"
                )
                st.session_state.wa_open = True

# opens WhatsApp automatically right after the summary is ready
if st.session_state.get("wa_open"):
    components.html(
        f"<script>window.open({json.dumps(st.session_state.wa_link)}, '_blank');</script>",
        height=0,
    )
    st.session_state.wa_open = False

# backup, hidden in a collapsed box
if st.session_state.get("wa_link"):
    with st.expander("See the summary / WhatsApp didn't open?"):
        st.write(st.session_state.summary)
        st.link_button("Open WhatsApp", st.session_state.wa_link)
        st.caption("📱 On a phone it opens WhatsApp directly. On a computer, log in to WhatsApp Web first, then press send.")

st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.whatsapp_number}")

if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if user_input:
    st.session_state.pop("wa_link", None)
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = []

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user", "image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user", "text", text)
        parts.append(text)
    elif photo is not None:
        parts.append("What is this meal? Give me the calories and macros.")

    with st.spinner("Crunching the numbers..."):
        answer = ask_gemini(parts)
    add_message("assistant", "text", answer)
    st.rerun()