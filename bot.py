import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

def generate_usernames(base):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    result = []

    for i in range(len(base) + 1):
        for huruf in alphabet:
            username = base[:i] + huruf + base[i:]
            result.append(f"@{username.lower()}")

    return result[:50]

def is_taken(username):
    try:
        r = requests.get(f"https://t.me/{username.strip('@')}", timeout=5)
        return r.status_code == 200
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim kata dasar username, contoh: ganteng")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kata = update.message.text.strip()
    if not kata.isalpha():
        await update.message.reply_text("Masukkan hanya huruf tanpa spasi atau simbol.")
        return

    await update.message.reply_text("Sedang memeriksa...")

    hasil = ""
    for username in generate_usernames(kata):
        status = "✅" if is_taken(username) else "❎"
        hasil += f"{username} {status}\n"

    for i in range(0, len(hasil), 4000):
        await update.message.reply_text(hasil[i:i+4000])

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
