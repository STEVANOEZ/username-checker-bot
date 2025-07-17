import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_usernames(base_word):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    results = set()
    for i in range(len(base_word) + 1):
        for char in alphabet:
            username = base_word[:i] + char + base_word[i:]
            results.add("@" + username)
    results.add("@" + base_word)
    return sorted(results)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim kata dasar username, contoh: ganteng")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh penggunaan: /check ganteng")
        return

    base_word = context.args[0].lower()
    usernames = generate_usernames(base_word)
    results = []

    for username in usernames:
        url = f"https://t.me/{username[1:]}"
        r = requests.get(url)
        if "If you have Telegram" in r.text or r.status_code == 200:
            results.append(f"{username} ✅")
        else:
            results.append(f"{username} ❎")

    await update.message.reply_text("\n".join(results[:40]))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    logger.info("Bot is running...")
    app.run_polling()
