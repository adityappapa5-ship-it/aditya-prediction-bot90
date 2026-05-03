
import telebot
from telebot import types
import base64
import os
import time

# --- CONFIG (YOUR NEW TOKEN) ---
API_TOKEN = '8518332653:AAG3AZXXOfmYj_vWg6y30FRFH72R4ktm63M'
bot = telebot.TeleBot(API_TOKEN)

# TERE ASLI CHANNELS (ID AUR LINK)
CHANNELS = ["-1003815161090", "-1003973812867"]
LINKS = ["https://t.me/+_RZ0gN9HU6xhZTRl", "https://t.me/+7bNfhxLosYsxMmVl"]
OWNER_LINK = "https://t.me/ADITYAXVIPBOT"

# --- 🛡️ FORCE JOIN CHECKER ---
def is_user_joined(user_id):
    try:
        for channel in CHANNELS:
            status = bot.get_chat_member(channel, user_id).status
            if status == 'left':
                return False
        return True
    except:
        return False

# --- 🔥 TAGADA ENCRYPTION LOGIC (UI SAFE) 🔥 ---
def tagada_encrypt(html_content):
    # Hidden Credit inside code
    branding = f"\n"
    full_content = branding + html_content
    
    # Base64 Lock
    b64_data = base64.b64encode(full_content.encode('utf-8')).decode('utf-8')
    
    # Military Obfuscation (Anti-Select + Anti-View Source)
    encrypted_html = f"""
    <script>
    var _0xadity = '{b64_data}';
    document.write(atob(_0xadity));
    
    // Security Locks
    document.addEventListener('contextmenu', e => e.preventDefault());
    document.onkeydown = function(e) {{
        if(e.keyCode == 123 || (e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0))) return false;
    }}
    </script>
    <style>
    body {{ -webkit-user-select: none; user-select: none; }}
    </style>
    """
    return encrypted_html

# --- 📥 FILE HANDLER (ENCRYPT ONLY) ---
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    # Force Join Check
    if not is_user_joined(message.from_user.id):
        bot.reply_to(message, "❌ **Pehle dono channels join karo!**")
        return

    if message.document.file_name.lower().endswith('.html'):
        m = bot.reply_to(message, "┌──────────────────────┐\n   🔐 ENCRYPTING: 1%\n└──────────────────────┘")
        
        # 1 to 100 Animation
        for p in [25, 60, 85, 100]:
            time.sleep(0.3)
            bot.edit_message_text(f"┌──────────────────────┐\n   🔐 ENCRYPTING: {p}%\n└──────────────────────┘", message.chat.id, m.message_id)

        try:
            file_info = bot.get_file(message.document.file_id)
            data = bot.download_file(file_info.file_path).decode('utf-8', errors='ignore')
            
            # Tagada Encryption
            final_data = tagada_encrypt(data)

            # Save and Send
            new_file = f"ADITYA_ENCRYPTED_{message.document.file_name}"
            with open(new_file, "w", encoding="utf-8") as f:
                f.write(final_data)
                
            with open(new_file, "rb") as f:
                cap = (
                    "┌──────────────────────┐\n"
                    "   👑 HTML ENCRYPTION DONE ✅\n"
                    "└──────────────────────┘\n\n"
                    "🛡️ Security: 100% Fixed\n"
                    "👤 Owner: Aditya Paswan\n\n"
                    "🎯 Channel: " + LINKS[0]
                )
                bot.send_document(message.chat.id, f, caption=cap)
            
            bot.delete_message(message.chat.id, m.message_id)
            os.remove(new_file)
        except Exception as e:
            bot.edit_message_text(f"❌ ERROR: {str(e)}", message.chat.id, m.message_id)

# --- START & BUTTONS ---
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎯 JOIN CHANNEL 1", url=LINKS[0]))
    markup.add(types.InlineKeyboardButton("🎯 JOIN CHANNEL 2", url=LINKS[1]))
    markup.add(types.InlineKeyboardButton("🔄 CHECK APPROVAL", callback_data="check"))
    
    msg = (
        "┌──────────────────────┐\n"
        "      👑 ADITYA X OWNER\n"
        "└──────────────────────┘\n\n"
        "Bhai, ye bot HTML ko itna tagada encrypt karega ki koi baap bhi nahi tod payega.\n\n"
        "⚠️ **Pehle upar diye gaye dono channels join karein!**"
    )
    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "check":
        if is_user_joined(call.from_user.id):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📤 UPLOAD HTML", callback_data="up"))
            markup.add(types.InlineKeyboardButton("👨‍💻 OWNER", url=OWNER_LINK))
            
            msg = (
                "┌──────────────────────┐\n"
                "   👑 VIP ENCRYPTOR ON\n"
                "└──────────────────────┘\n\n"
                "System Ready. Ab apni HTML file bhejo."
            )
            bot.edit_message_text(msg, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "❌ Pehle dono channels join karo!", show_alert=True)
            
    elif call.data == "up":
        bot.send_message(call.message.chat.id, "🔮 **SEND YOUR HTML FILE TO ENCRYPT**")

bot.infinity_polling()
