import requests
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_BOT_TOKEN = os.getenv("8261116719:AAH-ttQ8b26E07F1F55q4W3JHtEXnFowh5Q")
YOUTUBE_API_KEY = os.getenv("AIzaSyD9-Mx20sndFNiC4Yni3YcboNCfgRiqp6U")

app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot Running 24/7!"

def run():
    app_flask.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

def search_youtube(query):
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=5&q={query}&key={YOUTUBE_API_KEY}'
    data = requests.get(url).json()
    results = []
    for item in data.get('items', []):
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        results.append(f"{title}\n{video_url}")
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "@Chand_hackz 👇☠️\n\n"
        "└[ 🫶🏻 ]┘\n"
        "     ╰┈➤ 𝐇𝐞𝐲 !~ 𝐄𝐍𝐎𝐋𝐀 🐼🫶🏻\n\n"
        "𝐌𝐘 𝐍𝐀𝐌𝐄 𝐈𝐒 ~ ╰┈➤ Chand ☠️\n"
        "𝐈 𝐀𝐌 𝐓𝐇𝐄 𝐎𝐖𝐍𝐄𝐑 𝐎𝐅 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓\n\n"
        "RAT BOT 𝐀𝐑𝐄 100% 𝐖𝐎𝐑𝐊𝐈𝐍𝐆 🫶🏻\n\n"
        "     ❤️‍🩹!~ 𝐄𝐍𝐎𝐋𝐀❤️‍🩹\n\n"
        "🎮IF YOU HAVE ANY PROBLEM\n"
        "MESSAGE ADMIN :-\n\n"
        "╰┈➤🆔 @CHAND_HACKZ"
    )
    
    keyboard = [
        [KeyboardButton("💻 Hacking Search")],
        [KeyboardButton("📞 Contact Admin")],
        [KeyboardButton("ℹ️ Info")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_data = context.user_data

    if text == "💻 Hacking Search":
        await update.message.reply_text("Kya hacking related cheez search karna hai? Type karein:")
        user_data['awaiting_query'] = True

    elif user_data.get('awaiting_query'):
        results = search_youtube(text)
        if results:
            for result in results:
                await update.message.reply_text(result)
        else:
            await update.message.reply_text("Kuch nahi mila, dusra try karo.")
        user_data['awaiting_query'] = False

    elif text == "📞 Contact Admin":
        await update.message.reply_text("Contact: @Chand_hackz")

    elif text == "ℹ️ Info":
        await update.message.reply_text("Yeh bot hacking-related videos dhoondhne mein help karta hai!")

    else:
        await update.message.reply_text("Options mein se select karo 😊")

if __name__ == "__main__":
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Running 24/7...")
    app.run_polling()
