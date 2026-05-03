import telebot
from telebot import types
import time

# --- CONFIG ---
API_TOKEN = '8694242868:AAHw4p485GwDHnWQlxa7szVT8oqQZEtSf44' # ISSE CHANGE KAR LENA (SAFETY)
bot = telebot.TeleBot(API_TOKEN, parse_mode="MarkdownV2")

# --- UI DESIGN ---
START_TEXT = """
*╔══════════════════════╗*
* 👑 CHANNEL JOIN DECRYPT BOT 👑   *
*╚══════════════════════╝*

*Status:* 🟢 Online
*Developer:* [Aditya Paswan](https://t.me/your_link)

✨ *Aapka swagat hai\!* File decrypt karne ke liye niche button par click karke verification complete karein\.
"""

# --- HANDLERS ---

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("✅ VERIFICATION", callback_data="verify")
    markup.add(btn1)
    bot.send_message(message.chat.id, START_TEXT, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_user(call):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton("📤 UPLOAD FILE", callback_data="upload_mode")
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="*✅ Verification Successful\!\n\nAb apni HTML file yahan upload karein\.*",
        reply_markup=markup
    )

@bot.message_handler(content_types=['document'])
def process_file(message):
    if not message.document.file_name.endswith('.html'):
        bot.reply_to(message, "❌ *Error: Sirf \.html file upload karein\!*")
        return

    # Progress Bar Animation
    prog_msg = bot.send_message(message.chat.id, "🔍 *Processing: 0%*")
    
    for i in range(10, 101, 20):
        time.sleep(0.5)
        bar = "▓" * (i // 10) + "░" * (10 - (i // 10))
        bot.edit_message_text(
            f"⚡ *Decrypting File\.\.\.*\n\n`{bar}` *{i}%*",
            message.chat.id,
            prog_msg.message_id
        )

    # File Download & Decryption
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    content = downloaded_file.decode('utf-8', errors='ignore')

    # Basic Decryption Logic (Cleaning scripts/tags)
    # Aap yahan apna specific regex ya replacement logic badal sakte ho
    clean_content = content.replace('eval(unescape(', '').replace('document.write(unescape(', '')
    
    output_name = f"DECRYPTED_{message.document.file_name}"
    with open(output_name, "w", encoding="utf-8") as f:
        f.write(clean_content)

    # Send Back
    with open(output_name, "rb") as f:
        bot.send_document(
            message.chat.id, 
            f, 
            caption=f"✅ *File Decrypted By Aditya Paswan*\n\n*Name:* `{output_name}`"
        )
    
    bot.delete_message(message.chat.id, prog_msg.message_id)

bot.infinity_polling()
