import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "नमस्ते! 👋 मैं आपका अपना **BrainX Quiz Bot** हूँ।\n\nक्विज़ खेलने के लिए /quiz कमांड भेजें!"
    )

# /quiz कमांड जो ऑटोमैटिक पोल भेजेगा
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # यहाँ आप अपना सवाल सेट कर सकते हैं
    question = "भारत की राजधानी क्या है?"
    options = ["मुंबई", "नई दिल्ली", "कोलकाता", "चेन्नई"]
    correct_option_id = 1  # 1 का मतलब 'नई दिल्ली' सही है (गिनती 0 से शुरू होती है)

    await context.bot.send_poll(
        chat_id=chat_id,
        question=question,
        options=options,
        type="quiz",
        correct_option_id=correct_option_id,
        is_anonymous=False,
        explanation="सही उत्तर नई दिल्ली है!"
    )

def main():
    # सीधे आपके बॉट का टोकन यहाँ सेट है
    TOKEN = "8765282652:AAFBoehcJDeZvIX0H7AlLqhQXO935LqQifM"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))

    print("BrainX Quiz Bot 24/7 live हो गया है...")
    app.run_polling()

if __name__ == "__main__":
    main()
