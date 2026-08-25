import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render के लिए डमी वेब सर्वर ताकि सर्विस 24/7 एक्टिव रहे
async def handle(request):
    return web.Response(text="BrainX Quiz Bot is running successfully!")

async def web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "नमस्ते! 👋 मैं आपका अपना **BrainX Quiz Bot** हूँ।\n\nक्विज़ खेलने के लिए /quiz कमांड भेजें!"
    )

# /quiz कमांड जो ऑटोमैटिक पोल भेजेगा
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    question = "भारत की राजधानी क्या है?"
    options = ["मुंबई", "नई दिल्ली", "कोलकाता", "चेन्नई"]
    correct_option_id = 1  # नई दिल्ली सही जवाब

    await context.bot.send_poll(
        chat_id=chat_id,
        question=question,
        options=options,
        type="quiz",
        correct_option_id=correct_option_id,
        is_anonymous=False,
        explanation="सही उत्तर नई दिल्ली है!"
    )

async def main():
    # नया और फ्रेश बॉट टोकन यहाँ सेट है
    TOKEN = "8959348945:AAFTYLkJ-q40V46PR-InXwIG0qU3kpDLXig"
    
    # पहले वेब सर्वर शुरू करें
    await web_server()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))

    print("BrainX Quiz Bot 24/7 live हो गया है...")
    
    # बॉट रन करें (old updates को ड्रॉप करने के लिए)
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    # बॉट को चालू रखने के लिए
    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
