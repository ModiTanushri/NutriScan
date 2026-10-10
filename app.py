import asyncio
from telegram import Bot
import json
from google import genai
from google.genai import types
import streamlit as st 
from prompts import SYSTEM_PROMPT,WELCOME_MESSAGE_TEMPLATE,SUMMARY_REQUEST_PROMPT

NutriScan_API_Key=st.secrets["NutriScan_API_Key"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = NutriScan_API_Key)



gemini_client=get_gemini_client()

MODEL_NAME = "gemini-3.8-flash"

def clean_whatsapp_text(text):
    if not text:
        return "No nutrition summary available."
    text = " ".join(text.split())  #collapse whitespaces and newspaces
    return text[:1500] + "..." if len(text) > 1500 else text

def send_telegram(chat_id, user_name, summary):
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        text = f"Hi {user_name}! 👋\n\n{summary}"
        asyncio.run(bot.send_message(chat_id=chat_id, text=text[:4000]))
        return True, "sent"
    except Exception as error:
        return False, str(error)

def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"]=="text":
            st.write(message["content"])
        elif message["kind"]=="image":
            st.image(message["content"])

def add_message(role, kind, content):
    st.session_state.messages.append({"role":role, "kind":kind, "content":content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong : {error}"

#step 1: onboarding(username and phone)

if 'onboarded' not in st.session_state:
    st.title("NutriScan 🍱")
    st.caption("Snap it. Track it. Text yourself the result.")

    with st.form("onboarding_form"):
        name=st.text_input("Your name") 
        whatsapp_number=st.text_input(
            "Telegram Chat ID",
            placeholder="Enter your Telegram Chat ID",
            help="This is the number NutriScan will text your summary to."
        )

        submitted=st.form_submit_button("Let's go 👉")
    
    if submitted:
        if not  name.strip() or not whatsapp_number.strip():
            st.warning("Please enter your name and whatsapp number: ")

        else:
            st.session_state.name = name.strip( )
            st.session_state.whatsapp_number = whatsapp_number.strip( )
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

header_col, button_col = st.columns([5, 2], vertical_alignment = "center")

with header_col:
    st.title("NutriScan 🍱")

with button_col:
    send_disabled = len(st.session_state.messages) <= 2
    if st.button(
        "📤 Send to Telegram",
        disabled=send_disabled,
        help="Chat about at least one meal first" if send_disabled else None,
        use_container_width=True,
    ):
        summary = None
        with st.spinner("Summarizing your day..."):
            try:
                summary = ask_gemini([SUMMARY_REQUEST_PROMPT])
            except Exception as e:
                st.error(f"Couldn't create the summary: {e}")

        if summary:
            with st.spinner("Sending to Telegram..."):
                success, info = send_telegram(
                    st.session_state.whatsapp_number,
                    st.session_state.name,
                    summary[:1500],   
                )
            if success:
                st.success("Sent! Check your Telegram 📲")
                with st.expander("See what was sent"):
                    st.write(summary)
            else:
                st.error(f"Couldn't send that: {info}")

st.caption(f"Logged in as {st.session_state.name} - updates go to {st.session_state.whatsapp_number}")
 
if not st.session_state.messages:
    add_message("assistant", "text", WELCOME_MESSAGE_TEMPLATE.format(name=st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message)

user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type = ["jpg", "jpeg", "png"],
)

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text
    parts = [ ]

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

