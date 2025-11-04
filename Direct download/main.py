from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import os, requests

BOT_TOKEN = "8530861151:AAH9JX11RSgCgfWaMYlIgvBjg5KxOISMJZk"  # 🔹 अपना Token डालो
CHANNEL_USERNAME = "Digitalindia8"  # 🔹 बिना @ के Channel username
SERVER_URL = "https://your-app-name.onrender.com"  # 🔹 Render URL (deploy के बाद बदलना)

UPLOAD_DIR = "static"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def is_subscriber(user_id):
    """Check if the user is a member of the channel."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}"
    try:
        resp = requests.get(url).json()
        if resp.get("ok"):
            status = resp["result"]["status"]
            return status in ["member", "administrator", "creator"]
    except Exception:
        return False
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_subscriber(user_id):
        await update.message.reply_text("📤 स्वागत है! कोई भी फ़ाइल भेजो — मैं direct download link दूँगा।")
    else:
        await update.message.reply_text(f"❌ पहले हमारे चैनल को join करो:\n👉 t.me/{CHANNEL_USERNAME}")


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_subscriber(user_id):
        await update.message.reply_text(f"❌ पहले हमारे चैनल को join करो:\n👉 t.me/{CHANNEL_USERNAME}")
        return

    # Get file object (photo, doc, video etc.)
    file_obj = update.message.document or update.message.video or (
        update.message.photo[-1] if update.message.photo else None
    )

    if not file_obj:
        await update.message.reply_text("⚠️ कृपया कोई फ़ाइल भेजो।")
        return

    file_id = file_obj.file_id
    new_file = await context.bot.get_file(file_id)
    file_name = getattr(file_obj, "file_name", f"file_{file_id}.bin")
    file_path = os.path.join(UPLOAD_DIR, file_name)
    await new_file.download_to_drive(file_path)

    file_url = f"{SERVER_URL}/static/{file_name}"
    await update.message.reply_text(
        f"✅ फ़ाइल save हो गई!\n📎 `{file_name}`\n\n🔗 Download Link:\n{file_url}",
        parse_mode="Markdown",
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_file))

print("🤖 Bot started successfully!")
app.run_polling()
