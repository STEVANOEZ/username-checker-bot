import logging
import os
import itertools
import httpx
from time import sleep
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim kata dasar username, contoh: ganteng")

def generate_variations(base):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    results = set()
    for positions in itertools.product(alphabet, repeat=len(base) + 1):
        for i in range(len(base) + 1):
            s = base[:i] + positions[i] + base[i:]
            results.add(s)
    return list(results)

async def check_username(username):
    url = f"https://t.me/{username}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        return r.status_code != 200

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if not text.isalpha():
        await update.message.reply_text("Kirim hanya huruf tanpa spasi atau simbol.")
        return

    await update.message.reply_text("Mengecek username, tunggu sebentar...")

    candidates = generate_variations(text)[:10]
    result = ""
    for username in candidates:
        status = await check_username(username)
        emoji = "❎" if status else "✅"
        result += f"@{username} {emoji}\n"
        await sleep(0.5)

    await update.message.reply_text(result)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
