from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os, logging, requests

# Logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

def generate_usernames(base):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    results = set()
    for i in range(len(base) + 1):
        for c in alphabet:
            results.add(base[:i] + c + base[i:])
    return sorted(results)

def is_taken(uname):
    try:
        r = requests.get(f"https://t.me/{uname}", timeout=5)
        return r.status_code == 200
    except:
        return True

async def start(update, ctx):
    await update.message.reply_text("Kirim kata dasar (contoh: ganteng) atau gunakan /check <kata>")

async def check(update, ctx):
    if not ctx.args:
        return await start(update, ctx)
    await process_text(update, ctx, ctx.args[0].lower())

async def process_text(update, ctx, text):
    await update.message.reply_text(f"🔍 Mencari variasi untuk: {text}")
    usernames = generate_usernames(text)
    batch = ""
    for i, uname in enumerate(usernames, 1):
        marker = "✅" if is_taken(uname) else "❎"
        batch += f"@{uname} {marker}\n"
        if i % 20 == 0:
            await update.message.reply_text(batch)
            batch = ""
    if batch:
        await update.message.reply_text(batch)

async def handle_message(update, ctx):
    text = update.message.text.strip()
    if text.startswith("/"):
        return
    await process_text(update, ctx, text.lower())

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
