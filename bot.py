import os
import requests
import uuid
from telegram import Update, InlineQueryResultVideo
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, InlineQueryHandler

TOKEN = os.getenv("TOKEN")

cache = {}

def expand_url(short_url):
    r = requests.get(short_url, allow_redirects=True)
    return r.url

def get_video(url):
    url = expand_url(url)
    
    api_url = f"https://tikwm.com/api/?url={url}"
    response = requests.get(api_url).json()

    return response["data"]["play"], response["data"]["cover"]

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "tiktok.com" not in url:
        await update.message.reply_text("Please send a valid TikTok URL.")
        return

    if url in cache:
        await update.message.reply_video(cache[url])
        return

    try:
        video_url, video_cover = get_video(url)
        await update.message.reply_video(video=video_url)

    except Exception as e:
        await update.message.reply_text("Failed to download the TikTok video. Please try again.")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    if not query:
        return

    if "tiktok.com" not in query:
        return

    try:
        video_url, video_cover = get_video(query)

        results = [
            InlineQueryResultVideo(
                id=str(uuid.uuid4()),
                video_url=video_url,
                mime_type="video/mp4",
                thumbnail_url=video_cover,
                title="TikTok Video"
            )
        ]

        await update.inline_query.answer(results, cache_time=5)

    except Exception as e:
        print(e)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))
app.add_handler(InlineQueryHandler(inline_query))
print("Bot is running...")
app.run_polling()