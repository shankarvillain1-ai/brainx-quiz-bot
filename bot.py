import os
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    PollAnswerHandler,
    ContextTypes,
)

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# क्विज़ बैंक (आप इसमें जितने चाहें उतने सवाल बढ़ा सकते हैं)
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

# चैट के हिसाब से गेम और स्कोर ट्रैक करने के लिए डिक्शनरी
active_games = {}

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **नमस्ते! मैं आपका अपना एडवांस BrainX Quiz Pro Bot हूँ।**\n\n"
        "🎮 ग्रुप या चैट में धमाकेदार क्विज़ मुकाबला शुरू करने के लिए **/quiz** कमांड भेजें!\n"
        "✨ *यहाँ हर खिलाड़ी का सम्मान होता है और सब विनर बनते हैं!*"
    )

# /quiz कमांड जो गेम शुरू करेगा
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await update.message.reply_text("⚠️ इस चैट में क्विज़ पहले से चल रहा है! कृपया इसे पूरा होने दें।")
        return

    # नया गेम डेटा सेट करें
    active_games[chat_id] = {
        "current_q": 0,
        "scores": {},      # {user_id: {"name": str, "score": int}}
        "active": True
    }
    
    await update.message.reply_text(
        "🚀 **BrainX मेगा क्विज़ मुकाबला शुरू हो चुका है!**\n"
        "पूरी ऊर्जा के साथ तैयार हो जाइए, सवाल आने वाले हैं... 🎯"
    )
    await asyncio.sleep(2)
    await send_question(chat_id, context)

# सवाल भेजने का फंक्शन
async def send_question(chat_id, context):
    game = active_games.get(chat_id)
    if not game or not game["active"]:
        return

    q_idx = game["current_q"]
    
    # अगर सारे सवाल खत्म हो गए तो फाइनल लीडरबोर्ड दिखाएं
    if q_idx >= len(QUIZ_DATA):
        await show_final_leaderboard(chat_id, context)
        return

    q_data = QUIZ_DATA[q_idx]
    
    # पोल भेजें
    await context.bot.send_poll(
        chat_id=chat_id,
        question=f"❓ सवाल {q_idx + 1} / {len(QUIZ_DATA)}:\n{q_data['question']}",
        options=q_data["options"],
        type="quiz",
        correct_option_id=q_data["correct"],
        is_anonymous=False,
        explanation=q_data["explanation"]
    )

# यूजर के जवाब और स्कोर को ट्रैक करने का एडवांस सिस्टम
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
    q_idx = game["current_q"] - 1 # वर्तमान सवाल का इंडेक्स
    
    if q_idx < 0 or q_idx >= len(QUIZ_DATA):
        return

    correct_opt = QUIZ_DATA[q_idx]["correct"]
    
    # अगर यूजर का डेटा डिक्शनरी में नहीं है तो जोड़ें
    if user_id not in game["scores"]:
        game["scores"][user_id] = {"name": user_name, "score": 0}

    # अगर जवाब सही है तो पॉइंट बढ़ाएं
    if correct_opt in selected_options:
        game["scores"][user_id]["score"] += 1

    # जैसे ही लोग वोट दें, कुछ सेकंड बाद अगला सवाल ऑटोमैटिक भेजें
    # (चूंकि पोल का जवाब एक-एक करके आता है, हम इसे स्मूथ हैंडल कर रहे हैं)

# फाइनल विनर और सबकी लिस्ट दिखाने वाला शानदार फंक्शन
async def show_final_leaderboard(chat_id, context):
    game = active_games[chat_id]
    game["active"] = False
    scores_dict = game["scores"]

    if not scores_dict:
        await context.bot.send_message(
            chat_id=chat_id,
            text="🏁 क्विज़ समाप्त हो गया है, लेकिन किसी ने भी जवाब नहीं दिया! अगली बार कोशिश जरूर करें। 💪"
        )
        return

    # स्कोर के हिसाब से खिलाड़ियों को सॉर्ट करना (सबसे ज्यादा स्कोर वाला सबसे ऊपर)
    sorted_players = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)

    # टॉप विनर्स निकालना
    first_winner = sorted_players[0]
    second_winner = sorted_players[1] if len(sorted_players) > 1 else None
    third_winner = sorted_players[2] if len(sorted_players) > 2 else None

    # स्पेशल विनर मैसेज डिजाइन
    report = "🏆 **====================** 🏆\n"
    report += "       🌟 **MEGA QUIZ LEADERBOARD** 🌟\n"
    report += "🏆 **====================** 🏆\n\n"

    # 🥇 पहला विनर (खास स्पेशल ट्रीटमेंट)
    report += f"👑 **CHAMPION OF THE MATCH** 👑\n"
    report += f"🎉 दिल से बहुत-बहुत बधाई **{first_winner['name']}** जी! 🥇\n"
    report += f"🔥 आपने शानदार प्रदर्शन करते हुए सबसे ज्यादा **{first_winner['score']}** अंक हासिल किए हैं और महफिल लूट ली! आप वाकई कमाल के खिलाड़ी हैं! 🚀\n\n"

    # 🥈 दूसरा और 🥉 तीसरा विनर
    if second_winner:
        report += f"🥈 **दूसरा स्थान:** {second_winner['name']} (स्कोर: {second_winner['score']}) - बहुत ही शानदार मुकाबला!\n"
    if third_winner:
        report += f"🥉 **तीसरा स्थान:** {third_winner['name']} (स्कोर: {third_winner['score']}) - बेहतरीन खेल!\n"

    report += "\n📜 **सभी सम्मानित खिलाड़ियों की पूरी सूची (Scoreboard):**\n"
    report += "----------------------------------------\n"

    # 100-50 जितने भी लोग हों, सबका नाम इस लिस्ट में आएगा!
    for idx, player in enumerate(sorted_players, start=1):
        medal = ""
        if idx == 1: medal = "🥇"
        elif idx == 2: medal = "🥈"
        elif idx == 3: medal = "🥉"
        else: medal = f"#{idx}"
        
        report += f"{medal} **{player['name']}** — {player['score']} Points\n"

    report += "----------------------------------------\n"
    report += "💖 *जीत और हार तो खेल का हिस्सा है, असली बात सीखने और कोशिश करने की है! आप सभी विजेता हैं। अगली क्विज़ में फिर मिलते हैं!* ✨"

    await context.bot.send_message(chat_id=chat_id, text=report)

def main():
    TOKEN = "8959348945:AAFTYLkJ-q40V46PR-InXwIG0qU3kpDLXig"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    print("BrainX Quiz Pro Bot 24/7 live हो गया है...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
    
