import requests, telebot, time, random, os
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVER FOR 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "ADITYA VIP DIRECT LIVE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- CONFIG ---
API_TOKEN = '8601172080:AAFyWgSRVZT9a4NfwjwYSlyC6-s-q1ipTXY'
CHANNELS = [-1003815161090, -1003973812867]
WIN_STICKER = 'CAACAgUAAxkBAAERJRhp9B-PkyNlzscUNGUAAUchyXw63g8AAisSAAJSEdhVkI_Ixu7liJU7BA'
LOSS_STICKER = 'CAACAgUAAxkBAAERJRpp9B-X_XQ3vbejkVPLEIBkdKki-QACkBQAAiMYmVWHXHRU3FIjKzsE'
API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

bot = telebot.TeleBot(API_TOKEN)

def check_user_joined(uid):
    for c in CHANNELS:
        try:
            status = bot.get_chat_member(c, uid).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

def get_data_direct():
    h = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13)', 'Origin': 'https://ar-lottery01.com'}
    try:
        r = requests.get(API_URL, headers=h, timeout=12)
        return r.json().get('data', {}).get('list', [])
    except: return None

@bot.message_handler(commands=['start'])
def start(m):
    if check_user_joined(m.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 𝗚𝗘𝗧 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗜𝗢𝗡 𝗡𝗢𝗪 🚀"))
        bot.send_message(m.chat.id, "☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n\nStatus: <b>READY</b> ✅", parse_mode="HTML", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🚩 JOIN VIP CHANNEL", url="https://t.me/+45fCzXzXxi0zMWI9"))
        bot.send_message(m.chat.id, "❌ Join Kar Pehle!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🚀 𝗚𝗘𝗧 𝗣𝗥𝗘𝗗𝗜𝗖𝗧𝗜𝗢𝗡 𝗡𝗢𝗪 🚀")
def engine(message):
    # MAINE FALTU MESSAGES HATA DIYE HAIN. AB SEEDHA BOX AAYEGA.
    last_p = None
    bot.send_message(message.chat.id, "🔎 <b>Searching for Next Period...</b>", parse_mode="HTML")
    
    while True:
        try:
            history = get_data_direct()
            if history:
                curr_p = history[0]['issueNumber']
                if curr_p != last_p:
                    last_p = curr_p
                    next_p = int(curr_p) + 1
                    
                    # VIP Analysis logic
                    n = int(history[0]['number'])
                    pred = "🌕 𝗕𝗜𝗚" if n < 5 else "🌑 𝗦𝗠𝗔𝗟𝗟"
                    
                    # DIRECT PREDICTION BOX
                    box = (
                        f"☠️ <b>𝕬𝕯𝕴𝕿𝖄𝕬 𝖁𝕴𝕻 𝕮𝕽𝕬𝕮𝕶</b> 💀\n"
                        f"━━━━━━━━━━━━━━━━━━━\n"
                        f"🔢 <b>PERIOD:</b> <code>{next_p}</code>\n"
                        f"🎯 <b>PREDICT:</b> <b>{pred}</b>\n"
                        f"━━━━━━━━━━━━━━━━━━━"
                    )
                    bot.send_message(message.chat.id, box, parse_mode="HTML")
                    
                    time.sleep(55) # Result ka wait
                    check = get_data_direct()
                    if check and int(check[0]['issueNumber']) == next_p:
                        actual = "BIG" if int(check[0]['number']) >= 5 else "SMALL"
                        bot.send_sticker(message.chat.id, WIN_STICKER if pred.split()[1] == actual else LOSS_STICKER)
            time.sleep(5)
        except: time.sleep(10)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.remove_webhook()
    bot.infinity_polling()
    
