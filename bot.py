import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PollAnswerHandler,
    ContextTypes,
)
from aiohttp import web

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. Render के लिए एक असली Web Server (ताकि Port 8080 ओपन रहे और Render खुश रहे)
async def handle(request):
    return web.Response(text="BrainX Quiz Pro Bot is live and running 24/7!")

async def start_web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# क्विज़ डेटा बैंक
QUIZ_DATA = [
    {
        "question": "भारत की राजधानी क्या है?",
        "options": ["मुंबई", "नई दिल्ली", "कोलकाता", "चेन्नई"],
        "correct": 1,
        "explanation": "सही उत्तर नई दिल्ली है!"
    },
    {
        "question": "भारत का राष्ट्रीय खेल कौन सा है?",
        "options": ["क्रिकेट", "हॉकी", "कबड्डी", "फुटबॉल"],
        "correct": 1,
        "explanation": "सही उत्तर हॉकी है!"
    },
    {
        "question": "भारत का राष्ट्रीय पशु कौन सा है?",
        "options": ["शेर", "हाथी", "बाघ", "चीता"],
        "correct": 2,
        "explanation": "सही उत्तर बाघ (Tiger) है!"
    },
    {
        "question": "कंप्यूटर का दिमाग किसे कहा जाता है?",
        "options": ["CPU", "RAM", "Hard Disk", "Monitor"],
        "correct": 0,
        "explanation": "सही उत्तर CPU है!"
    },
    {
        "question": "सौर मंडल का सबसे बड़ा ग्रह कौन सा है?",
        "options": ["मंगल", "शनि", "बृहस्पति (Jupiter)", "पृथ्वी"],
        "correct": 2,
        "explanation": "सही उत्तर बृहस्पति (Jupiter) है!"
    }
]

active_games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **नमस्ते! मैं आपका अपना एडवांस BrainX Quiz Pro Bot हूँ।**\n\n"
        "🎮 ग्रुप या चैट में धमाकेदार क्विज़ मुकाबला शुरू करने के लिए **/quiz** कमांड भेजें!\n"
        "✨ *यहाँ हर खिलाड़ी का सम्मान होता है और सब विनर बनते हैं!*"
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await update.message.reply_text("⚠️ इस चैट में क्विज़ पहले से चल रहा है! कृपया इसे पूरा होने दें।")
        return

    active_games[chat_id] = {
        "current_q": 0,
        "scores": {},
        "active": True
    }
    
    await update.message.reply_text(
        "🚀 **BrainX मेगा क्विज़ मुकाबला शुरू हो चुका है!**\n"
        "तैयार हो जाइए, पहला सवाल आ रहा है... 🎯"
    )
    await send_question(chat_id, context)

async def send_question(chat_id, context):
    game = active_games.get(chat_id)
    if not game or not game["active"]:
        return

    q_idx = game["current_q"]
    
    if q_idx >= len(QUIZ_DATA):
        await show_final_leaderboard(chat_id, context)
        return

    q_data = QUIZ_DATA[q_idx]
    
    await context.bot.send_poll(
        chat_id=chat_id,
        question=f"❓ सवाल {q_idx + 1} / {len(QUIZ_DATA)}:\n{q_data['question']}",
        options=q_data["options"],
        type="quiz",
        correct_option_id=q_data["correct"],
        is_anonymous=False,
        explanation=q_data["explanation"]
    )

async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user
    user_id = user.id
    user_name = user.first_name if user.first_name else "Khiladi"
    selected_options = answer.option_ids
    
    chat_id = None
    for cid, g in active_games.items():
        if g["active"]:
            chat_id = cid
            break
            
    if not chat_id:
        return

    game = active_games[chat_id]
    q_idx = game["current_q"] - 1
    
    if q_idx < 0 or q_idx >= len(QUIZ_DATA):
        return

    correct_opt = QUIZ_DATA[q_idx]["correct"]
    
    if user_id not in game["scores"]:
        game["scores"][user_id] = {"name": user_name, "score": 0}

    if correct_opt in selected_options:
        game["scores"][user_id]["score"] += 1

async def show_final_leaderboard(chat_id, context):
    game = active_games[chat_id]
    game["active"] = False
    scores_dict = game["scores"]

    if not scores_dict:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🏁 क्विज़ समाप्त हो गया है, लेकिन किसी ने जवाब नहीं दिया! अगली बार कोशिश जरूर करें। 💪"
        )
        return

    sorted_players = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)
    first_winner = sorted_players[0]
    second_winner = sorted_players[1] if len(sorted_players) > 1 else None
    third_winner = sorted_players[2] if len(sorted_players) > 2 else None

    report = "🏆 **====================** 🏆\n"
    report += "       🌟 **MEGA QUIZ LEADERBOARD** 🌟\n"
    report += "🏆 **====================** 🏆\n\n"

    report += f"👑 **CHAMPION OF THE MATCH** 👑\n"
    report += f"🎉 बहुत-बहुत बधाई **{first_winner['name']}** जी! 🥇\n"
    report += f"🔥 सबसे ज्यादा **{first_winner['score']}** अंक हासिल करके आपने महफिल लूट ली! 🚀\n\n"

    if second_winner:
        report += f"🥈 **दूसरा स्थान:** {second_winner['name']} (स्कोर: {second_winner['score']})\n"
    if third_winner:
        report += f"🥉 **तीसरा स्थान:** {third_winner['name']} (स्कोर: {third_winner['score']})\n"

    report += "\n📜 **सभी खिलाड़ियों का स्कोरबोर्ड:**\n"
    report += "----------------------------------------\n"

    for idx, player in enumerate(sorted_players, start=1):
        medal = f"🥇" if idx == 1 else f"🥈" if idx == 2 else f"🥉" if idx == 3 else f"#{idx}"
        report += f"{medal} **{player['name']}** — {player['score']} Points\n"

    report += "----------------------------------------\n"
    report += "💖 *जीत और हार खेल का हिस्सा है, कोशिश करने वाले सब विनर हैं!* ✨"

    await context.bot.send_message(chat_id=chat_id, text=report)

async def main():
    TOKEN = "8959348945:AAFTYLkJ-q40V46PR-InXwIG0qU3kpDLXig"
    
    # सबसे पहले वेब सर्वर शुरू करें ताकि Render का पोर्ट एरर हमेशा के लिए खत्म हो जाए
    await start_web_server()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    print("BrainX Quiz Pro Bot live & running...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
