import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔑 Token bot Telegram (thay bằng token của bạn)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ======================= CÁC LỆNH =======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Xin chào! Tôi là bot tải video.\n"
        "Gõ /help để xem hướng dẫn."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Các lệnh có thể dùng:\n"
        "/tiktok <link>\n"
        "/fb <link>\n"
        "/yt <link>\n"
        "Bot sẽ trả về link tải video."
    )

# ======================= HÀM LẤY LINK =======================

def get_download_link(url):
    """
    Dùng snapvideo.co hoặc taivideo.vn để lấy link tải video.
    Đây chỉ là ví dụ scraping đơn giản -> Có thể thay đổi tùy site.
    """
    try:
        r = requests.get("https://taivideo.vn", params={"url": url}, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Tìm thẻ <a> có chứa link video
        a_tag = soup.find("a", href=True)
        if a_tag:
            return a_tag["href"]
        return None
    except Exception as e:
        print("Error:", e)
        return None

# ======================= LỆNH CHÍNH =======================

async def tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Bạn cần nhập link TikTok.\nVí dụ: /tiktok https://...")
        return
    url = context.args[0]
    dl = get_download_link(url)
    if dl:
        await update.message.reply_text(f"✅ Link tải: {dl}")
    else:
        await update.message.reply_text("❌ Không lấy được link. Thử lại sau.")

async def fb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Bạn cần nhập link Facebook.\nVí dụ: /fb https://...")
        return
    url = context.args[0]
    dl = get_download_link(url)
    if dl:
        await update.message.reply_text(f"✅ Link tải: {dl}")
    else:
        await update.message.reply_text("❌ Không lấy được link. Thử lại sau.")

async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Bạn cần nhập link YouTube.\nVí dụ: /yt https://...")
        return
    url = context.args[0]
    dl = get_download_link(url)
    if dl:
        await update.message.reply_text(f"✅ Link tải: {dl}")
    else:
        await update.message.reply_text("❌ Không lấy được link. Thử lại sau.")

# ======================= MAIN =======================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("tiktok", tiktok))
    app.add_handler(CommandHandler("fb", fb))
    app.add_handler(CommandHandler("yt", yt))

    print("🤖 Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
