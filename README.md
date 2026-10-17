# NutriScan 
NutriScan is an AI-Based Nutrition buddy that helps to estimate calories and macros in our food.
Upload a photo of a meal or describe what you serve, get rough estimate of calories and macros, tips for healthy life and send the chat summary to your WhatsApp.

**Live App**: https://nutriscan-01.streamlit.app

##  Built with
- Python
- Streamlit
- Google Gemini (chat and image understanding)
- WhatsApp click-to-chat link

## Features:
**Photo analysis:** Upload a meal and get an analysis of calories, macros and tips for healthy life.
**Chat by texting:** Describe a meal like 'Rice with dal' or ask a question related to food .
**Suggestions:** Get some tips to balance diet and to lead a healthy life.
**Friendly and food focused:** If you ask unrelated to food, get a reply in polite way.
**Summary:** One button sends a summary of our chat to WhatsApp for reference. 

##  Run it locally
1. Clone this repository.
2. Install the packages: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with your Gemini API key, using the names that `app.py` reads.
4. Run: `streamlit run app.py` or 'python -m streamlit run app.py'


## How to use NutriScan?
1. Open https://nutriscan-01.streamlit.app
2. Enter your **name** and your **WhatsApp number** with country code (for India, 91 followed by your 10 digits, like 919876543210), then click **Let's go**.
3. Upload a meal photo or type what you ate.
   - **Tip:** use a photo under 1 MB for a faster reply.
4. Keep chatting about your meals as long as you like.
5. Click **Send to WhatsApp**. NutriScan prepares your summary and opens WhatsApp with it already typed.
6. Press **send** in WhatsApp. The message goes to your own chat.
   - **On a phone:** it opens the WhatsApp app directly.
   - **On a computer:** log in to WhatsApp Web or WhatsApp Desktop first.

If WhatsApp doesn't open by itself, open the small box under the button (**See the summary / WhatsApp didn't open?**) and click **Open WhatsApp**.


---

## Fault-finding
| Problem | What to do |
|---|---|
| Message says to chat first | Chat about at least one meal, then click **Send to WhatsApp** again. |
| WhatsApp doesn't open by itself | Your browser may have blocked the pop-up. Click the pop-up icon in the address bar and choose **Always allow**, or use the **Open WhatsApp** button in the small box. |
| WhatsApp shows an invalid number | Enter your number with the country code and no `+` or spaces. |
| The link doesn't open WhatsApp on a computer | Install WhatsApp Desktop or log in to web.whatsapp.com, then try again. |
| Photo takes a long time | Use a smaller photo (under 1 MB). |

---

##  Disclaimer
NutriScan gives rough estimates from photos and descriptions. They are not exact and are not medical or dietary advice. For health conditions or special diets, please talk to a doctor or a registered dietitian.

---



