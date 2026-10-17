# NutriScan 
NutriScan is an AI-Based Nutrition buddy that helps to estimate calories and macros in our food.
Upload a photo of a meal or describe what you serve, get rough estimate of calories and macros, tips for healthy life and send the chat summary to your Telegram.

**Live App**: https://nutriscan-01.streamlit.app

##  Built with
- Python
- Streamlit
- Google Gemini (chat and image understanding)
- Telegram Bot API

## Features:
**Photo analysis:** Upload a meal and get an analysis of calories, macros and tips for healthy life.
**Chat by texting:** Describe a meal like 'Rice with dal' or ask a question related to food .
**Suggestions:** Get some tips to balance diet and to lead a healthy life.
**Friendly and food focused:** If you ask unrelated to food, get a reply in polite way.
**Summary:** One button sends a summary of our chat to Telegram for reference.

##  Run it locally
1. Clone this repository.
2. Install the packages: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with your Gemini API key and Telegram bot token, using the names that `app.py` reads.
4. Run: `streamlit run app.py`


## How to use NutriScan?
### Step 1: Get Telegram chat ID
Chat ID is a number that get from a Telegram, you don't need to create create bot.

1: Open Telegram and search for **@userinfobot**, then press **Start**.
2. It replies with your details. Copy the number next to **Id**. That is your chat ID.

### Step 2: Start our bot (needed once)
Telegram only lets a bot message you after you press Start.

1. Open **@Our_NutriScan_bot** in Telegram.
2. Press **Start**.

### Step 3: Open the app
1. Go to https://nutriscan-01.streamlit.app
2. Enter your **name** and your **Telegram chat ID**, then start.

### Step 4: Chat about your meals
- Upload a meal photo, or type what you ate.
- **Tip:** use a photo under 1 MB for a faster reply.
- Read the estimates and tips in the reply.

### Step 5: Send the summary to Telegram
Chat about at least one meal, then click the **Send to Telegram** button. The summary arrives in your Telegram chat.

---

## Fault-finding
| Problem | What to do |
|---|---|
| Summary doesn't arrive | Open our bot in Telegram and press **Start** first. |
| "Chat not found" error | Check that your chat ID is the number from @userinfobot, with no spaces or letters. |
| Photo takes a long time | Use a smaller photo (under 1 MB). |
| Button is greyed out | Chat about a meal first. The button turns on after a few messages. |

---

##  Disclaimer
NutriScan gives rough estimates from photos and descriptions. They are not exact and are not medical or dietary advice. For health conditions or special diets, please talk to a doctor or a registered dietitian.

---



