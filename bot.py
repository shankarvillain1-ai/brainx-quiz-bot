import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    PollAnswerHandler,
    ContextTypes,
    filters
)
from aiohttp import web

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render के लिए Web Server
async def handle(request):
    return web.Response(text="BrainX Ultimate Quiz Pro Bot is live and running 24/7!")

async def start_web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ==================== FULL QUESTION BANKS ====================

GK_QUESTIONS = [
    {"question": "भारत का राष्ट्रीय गीत 'वंदे मातरम' किसने लिखा है?", "options": ["बंकिम चंद्र चट्टोपाध्याय", "रविंद्रनाथ टैगोर", "इक़बाल", "सरदार पटेल"], "correct": 0, "explanation": "वंदे मातरम बंकिम चंद्र चट्टोपाध्याय द्वारा आनंदमठ से लिया गया है।"},
    {"question": "भारत का संविधान कब लागू हुआ?", "options": ["15 अगस्त 1947", "26 जनवरी 1950", "26 नवंबर 1949", "2 अक्टूबर 1952"], "correct": 1, "explanation": "भारत का संविधान 26 जनवरी 1950 को पूर्ण रूप से लागू हुआ था।"},
    {"question": "महात्मा गांधी ने असहयोग आंदोलन किस वर्ष शुरू किया था?", "options": ["1920", "1922", "1930", "1942"], "correct": 0, "explanation": "असहयोग आंदोलन की शुरुआत 1920 में महात्मा गांधी ने की थी।"},
    {"question": "भारत में सबसे लंबी नदी कौन सी है?", "options": ["यमुना", "ब्रह्मपुत्र", "गंगा", "गोदावरी"], "correct": 2, "explanation": "गंगा भारत की सबसे लंबी नदी है।"},
    {"question": "किस ग्रह को 'लाल ग्रह' कहा जाता है?", "options": ["शुक्र", "मंगल", "बुध", "शनि"], "correct": 1, "explanation": "आयरन ऑक्साइड की अधिकता के कारण मंगल ग्रह को लाल ग्रह कहते हैं।"},
    {"question": "भारत के प्रथम प्रधानमंत्री कौन थे?", "options": ["डॉ. राजेंद्र प्रसाद", "जवाहरलाल नेहरू", "वल्लभभाई पटेल", "लाल बहादुर शास्त्री"], "correct": 1, "explanation": "पंडित जवाहरलाल नेहरू भारत के प्रथम प्रधानमंत्री थे।"},
    {"question": "कंप्यूटर का आविष्कार किसने किया था?", "options": ["चार्ल्स बेबेज", "अल्बर्ट आइंस्टीन", "थॉमस एडिसन", "आइज़ैक न्यूटन"], "correct": 0, "explanation": "चार्ल्स बेबेज को कंप्यूटर का जनक कहा जाता है।"},
    {"question": "राष्ट्रीय विज्ञान दिवस कब मनाया जाता है?", "options": ["28 फरवरी", "5 सितंबर", "15 अगस्त", "26 जनवरी"], "correct": 0, "explanation": "28 फरवरी को राष्ट्रीय विज्ञान दिवस मनाया जाता है।"},
    {"question": "भारत का राष्ट्रीय पशु क्या है?", "options": ["शेर", "हाथी", "बाघ", "चीता"], "correct": 2, "explanation": "भारत का राष्ट्रीय पशु बाघ (Tiger) है।"},
    {"question": "क्षेत्रफल की दृष्टि से भारत का सबसे बड़ा राज्य कौन सा है?", "options": ["महाराष्ट्र", "उत्तर प्रदेश", "राजस्थान", "मध्य प्रदेश"], "correct": 2, "explanation": "क्षेत्रफल की दृष्टि से राजस्थान सबसे बड़ा राज्य है।"}
]

HINDI_QUESTIONS = [
    {"question": "'विद्यालय' शब्द का सही संधि विच्छेद क्या है?", "options": ["विद्या + आलय", "विध + आलय", "विद्य + लय", "विद्या + लय"], "correct": 0, "explanation": "विद्यालय दीर्घ स्वर संधि का उदाहरण है।"},
    {"question": "हिंदी वर्णमाला में कुल कितने स्वर होते हैं?", "options": ["10", "11", "13", "12"], "correct": 1, "explanation": "मानक हिंदी वर्णमाला में कुल 11 स्वर होते हैं।"},
    {"question": "'कमल' का पर्यायवाची शब्द इनमें से कौन सा है?", "options": ["जलद", "पंकज", "नीरद", "वारिधि"], "correct": 1, "explanation": "पंकज कमल का पर्यायवाची है।"},
    {"question": "जिसकी कोई उपमा न हो, उसे क्या कहते हैं?", "options": ["अनुपम", "अद्भुत", "सुंदर", "अद्वितीय"], "correct": 0, "explanation": "जिसकी कोई उपमा न हो उसे अनुपम कहते हैं।"},
    {"question": "'घोड़ा' का बहुवचन रूप क्या होगा?", "options": ["घोड़ें", "घोड़े", "घोड़ो", "घोड़ी"], "correct": 1, "explanation": "घोड़ा का बहुवचन 'घोड़े' होता है।"}
]

ENGLISH_QUESTIONS = [
    {"question": "What is the antonym of 'Brave'?", "options": ["Coward", "Bold", "Fearless", "Courageous"], "correct": 0, "explanation": "Coward is the opposite (antonym) of brave."},
    {"question": "Choose the correct spelling:", "options": ["Recieve", "Receive", "Riciive", "Receeve"], "correct": 1, "explanation": "The correct spelling is Receive."},
    {"question": "He ___ to school every day. (Fill in the blank)", "options": ["go", "gone", "goes", "going"], "correct": 2, "explanation": "With singular third-person 'He', we use 'goes'."},
    {"question": "What is the synonym of 'Happy'?", "options": ["Sad", "Joyful", "Angry", "Tired"], "correct": 1, "explanation": "Joyful has a similar meaning to happy."},
    {"question": "Identify the noun in the sentence: 'The cat slept on the mat.'", "options": ["Slept", "On", "Cat", "The"], "correct": 2, "explanation": "'Cat' is a noun in the sentence."}
]

ART_QUESTIONS = [
    {"question": "ताजमहल का डिजाइन किसने तैयार किया था?", "options": ["उस्ताद अहमद लाहौरी", "उस्ताद ईसा", "शाहजहाँ", "बीरबल"], "correct": 0, "explanation": "ताजमहल के मुख्य वास्तुकार उस्ताद अहमद लाहौरी थे।"},
    {"question": "कथकली नृत्य किस राज्य से संबंधित है?", "options": ["उत्तर प्रदेश", "केरल", "तमिलनाडु", "आंध्र प्रदेश"], "correct": 1, "explanation": "कथकली केरल का प्रमुख शास्त्रीय नृत्य है।"},
    {"question": "कोणार्क का सूर्य मंदिर किस राज्य में स्थित है?", "options": ["उड़ीसा", "कर्नाटक", "राजस्थान", "गुजरात"], "correct": 0, "explanation": "कोणार्क का सूर्य मंदिर ओडिशा में स्थित है।"},
    {"question": "मधुबनी चित्रकला शैली किस राज्य से प्रसिद्ध है?", "options": ["बिहार", "पश्चिम बंगाल", "मध्य प्रदेश", "पंजाब"], "correct": 0, "explanation": "मधुबनी कला बिहार के मिथिला क्षेत्र से जुड़ी है।"},
    {"question": "कुचिपुड़ी किस राज्य का शास्त्रीय नृत्य है?", "options": ["केरल", "आंध्र प्रदेश", "ओडिशा", "मणिपुर"], "correct": 1, "explanation": "कुचिपुड़ी आंध्र प्रदेश का शास्त्रीय नृत्य है।"}
]

user_custom_quizzes = {}
creating_state = {}
active_games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **नमस्ते! आपका स्वागत है BrainX Quiz Pro Bot में।**\n\n"
        "🎮 **प्री-बिल्ड क्विज़ कमांड्स:**\n"
        "👉 `/gkquiz` - GK Quiz\n"
        "👉 `/hindiquiz` - Hindi Quiz\n"
        "👉 `/englishquiz` - English Quiz\n"
        "👉 `/artquiz` - Art & Culture Quiz\n\n"
        "💡 **इंस्टेंट पोल मेकर:**\n"
        "मैसेज में इस तरह भेजकर तुरंत पोल बनाएँ:\n"
        "`सवाल यहाँ लिखें?`\n"
        "`ऑप्शन 1, ऑप्शन 2, ऑप्शन 3, ऑप्शन 4`\n"
        "`सही विकल्प का नंबर (जैसे 1)`\n\n"
        "📌 **अन्य कमांड्स:**\n"
        "👉 `/createquiz` - स्टेप-बाय-स्टेप क्विज़ बनाएँ\n"
        "👉 `/myquiz` - अपनी बनाई क्विज़ खेलें\n"
        "👉 `/stopquiz` - चल रही क्विज़ रोकें\n\n"
        "👑 **Bot Creator & Developed By:** @krishnazxy",
        parse_mode="Markdown"
    )

async def start_quiz_session(update: Update, context: ContextTypes.DEFAULT_TYPE, q_list, quiz_name):
    chat_id = update.effective_chat.id
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await update.message.reply_text("⚠️ इस चैट में पहले से क्विज़ चल रहा है! कृपया इसे पूरा होने दें या `/stopquiz` भेजें।")
        return

    active_games[chat_id] = {
        "questions": q_list,
        "quiz_name": quiz_name,
        "current_q": 0,
        "scores": {},
        "active": True
    }
    
    await update.message.reply_text(
        f"🚀 **{quiz_name} की मेगा क्विज़ शुरू हो चुकी है!**\n"
        f"🎯 कुल प्रश्न: {len(q_list)} | हर सवाल के लिए 15 सेकंड का समय है।"
    )
    await asyncio.sleep(1)
    await send_next_question(chat_id, context)

async def gk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, GK_QUESTIONS, "GK Quiz")

async def hindi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, HINDI_QUESTIONS, "Hindi Quiz")

async def english_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, ENGLISH_QUESTIONS, "English Quiz")

async def art_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, ART_QUESTIONS, "Art & Culture Quiz")

async def send_next_question(chat_id, context):
    game = active_games.get(chat_id)
    if not game or not game["active"]:
        return

    q_idx = game["current_q"]
    q_list = game["questions"]
    
    if q_idx >= len(q_list):
        await show_final_leaderboard(chat_id, context)
        return

    q_data = q_list[q_idx]
    
    await context.bot.send_poll(
        chat_id=chat_id,
        question=f"[{game['quiz_name']}] प्रश्न {q_idx + 1} / {len(q_list)}:\n{q_data['question']}",
        options=q_data["options"],
        type="quiz",
        correct_option_id=q_data["correct"],
        is_anonymous=False,
        explanation=q_data["explanation"],
        open_period=15
    )
    
    game["current_q"] += 1
    await asyncio.sleep(16)
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await send_next_question(chat_id, context)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) >= 3 and chat_id not in creating_state:
        question_text = lines[0]
        options = [opt.strip() for opt in lines[1].split(",")]
        correct_ans_str = lines[2].lower()
        
        correct_index = 0
        if correct_ans_str.isdigit():
            correct_index = int(correct_ans_str) - 1
        else:
            for idx, opt in enumerate(options):
                if opt.lower() == correct_ans_str:
                    correct_index = idx
                    break

        if len(options) >= 2 and 0 <= correct_index < len(options):
            await context.bot.send_poll(
                chat_id=chat_id,
                question=f"💡 [Instant Poll by @krishnazxy]\n{question_text}",
                options=options,
                type="quiz",
                correct_option_id=correct_index,
                is_anonymous=False,
                explanation="यह पोल आपके द्वारा भेजे गए टेक्स्ट से बनाया गया है!"
            )
            return

    if chat_id not in creating_state:
        return

    state = creating_state[chat_id]
    step = state["step"]

    if step == "get_title":
        state["title"] = text
        state["step"] = "get_question"
        await update.message.reply_text(f"✅ क्विज़ का नाम: **{text}** सेट हो गया है।\n\nअब अपने **पहले सवाल (Question)** को लिखकर भेजें:")

    elif step == "get_question":
        state["current_q"] = text
        state["step"] = "get_options"
        await update.message.reply_text("अब इस सवाल के **4 विकल्प (Options)** कॉमा (,) लगाकर भेजें:")

    elif step == "get_options":
        options = [opt.strip() for opt in text.split(",")]
        if len(options) < 2:
            await update.message.reply_text("⚠️ कृपया कम से कम 2 विकल्प सही फॉर्मेट में भेजें:")
            return
        state["current_options"] = options
        state["step"] = "get_correct"
        await update.message.reply_text("अब सही विकल्प का **नंबर** (जैसे 1 या 2) लिखकर भेजें:")

    elif step == "get_correct":
        try:
            correct_num = int(text.strip()) - 1
            options = state["current_options"]
            if not (0 <= correct_num < len(options)):
                raise ValueError()
        except ValueError:
            await update.message.reply_text("⚠️ कृपया सही विकल्प का मान्य नंबर भेजें:")
            return

        state["current_correct"] = correct_num
        state["step"] = "get_explanation"
        await update.message.reply_text("💡 अब इस सवाल का **स्पष्टीकरण (Explanation)** लिखकर भेजें:")

    elif step == "get_explanation":
        explanation = text.strip()
        state["questions"].append({
            "question": state["current_q"],
            "options": state["current_options"],
            "correct": state["current_correct"],
            "explanation": explanation
        })

        state["step"] = "ask_more"
        keyboard = [
            [InlineKeyboardButton("➕ और सवाल जोड़ें", callback_data="add_more_q")],
            [InlineKeyboardButton("✅ क्विज़ समाप्त और सेव करें", callback_data="finish_my_quiz")]
        ]
        await update.message.reply_text(f"✅ सवाल जुड़ गया! कुल सवाल: **{len(state['questions'])}**", reply_markup=InlineKeyboardMarkup(keyboard))

async def create_quiz_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    creating_state[chat_id] = {"step": "get_title", "questions": []}
    await update.message.reply_text("📝 **नई क्विज़ बनाने की प्रक्रिया शुरू!** अपनी इस क्विज़ का **शीर्षक (Title)** भेजें:")

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "add_more_q":
        if chat_id in creating_state:
            creating_state[chat_id]["step"] = "get_question"
            await query.message.reply_text("📝 अगला नया सवाल भेजें:")

    elif query.data == "finish_my_quiz":
        if chat_id in creating_state:
            quiz_data = creating_state[chat_id]
            user_custom_quizzes[chat_id] = quiz_data
            keyboard = [[InlineKeyboardButton("🚀 इस क्विज़ को खेलें", callback_data="play_my_quiz")]]
            await query.message.edit_text(
                f"🎉 **कस्टम क्विज़ तैयार है!**\n📌 **नाम:** {quiz_data['title']}\n📊 **कुल प्रश्न:** {len(quiz_data['questions'])}\n👑 **Created by:** @krishnazxy",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            del creating_state[chat_id]

    elif query.data == "play_my_quiz":
        if chat_id in user_custom_quizzes:
            await start_quiz_session(update, context, user_custom_quizzes[chat_id]["questions"], user_custom_quizzes[chat_id]["title"])

async def play_my_quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in user_custom_quizzes:
        await start_quiz_session(update, context, user_custom_quizzes[chat_id]["questions"], user_custom_quizzes[chat_id]["title"])
    else:
        await update.message.reply_text("⚠️ आपकी कोई कस्टम क्विज़ नहीं मिली। `/createquiz` से बनाएँ!")

async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user
    user_id = user.id
    user_name = user.first_name if user.first_name else "Khiladi"
    selected_options = answer.option_ids

    for chat_id, game in active_games.items():
        if game["active"]:
            q_idx = game["current_q"] - 1
            q_list = game["questions"]
            if 0 <= q_idx < len(q_list):
                correct_opt = q_list[q_idx]["correct"]
                if user_id not in game["scores"]:
                    game["scores"][user_id] = {"name": user_name, "score": 0}
                if correct_opt in selected_options:
                    game["scores"][user_id]["score"] += 1

async def stop_quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_games and active_games[chat_id]["active"]:
        active_games[chat_id]["active"] = False
        await update.message.reply_text("🛑 **क्विज़ रोक दी गई है!**")
        await show_final_leaderboard(chat_id, context)
    else:
        await update.message.reply_text("⚠️ इस समय कोई क्विज़ सक्रिय नहीं है।")

async def show_final_leaderboard(chat_id, context):
    game = active_games[chat_id]
    game["active"] = False
    scores_dict = game["scores"]
    quiz_name = game["quiz_name"]

    report = f"🏆 **====================** 🏆\n"
    report += f"   🌟 **{quiz_name.upper()} LEADERBOARD** 🌟\n"
    report += f"🏆 **====================** 🏆\n\n"

    report += f"👑 **Bot Developed & Created By:** @krishnazxy 🚀\n\n"

    if not scores_dict:
        report += "🏁 क्विज़ समाप्त! किसी ने उत्तर दर्ज नहीं किया।\n"
    else:
        sorted_players = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)
        first_winner = sorted_players[0]

        report += f"🎉 **चैंपियन विनर:** {first_winner['name']} (स्कोर: {first_winner['score']}) 🥇\n\n"
        report += "📜 **सभी खिलाड़ियों की सूची (Scoreboard):**\n"
        report += "----------------------------------------\n"
        for idx, player in enumerate(sorted_players, start=1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
            report += f"{medal} **{player['name']}** — {player['score']} Points\n"
        report += "----------------------------------------\n"

    report += "💖 *जीत-हार खेल का हिस्सा है, आप सभी शानदार खिलाड़ी हैं!* ✨"
    await context.bot.send_message(chat_id=chat_id, text=report)

async def main():
    # 🔒 आपका नया सुरक्षित टोकन अपडेट कर दिया गया है
    TOKEN = "8959348945:AAEMMcO3jXYeI5ylymY2dJE75NAqYxJPbxY"
    
    await start_web_server()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gkquiz", gk_cmd))
    app.add_handler(CommandHandler("hindiquiz", hindi_cmd))
    app.add_handler(CommandHandler("englishquiz", english_cmd))
    app.add_handler(CommandHandler("artquiz", art_cmd))
    app.add_handler(CommandHandler("createquiz", create_quiz_start))
    app.add_handler(CommandHandler("myquiz", play_my_quiz_cmd))
    app.add_handler(CommandHandler("stopquiz", stop_quiz_cmd))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    app.add_handler(CallbackQueryHandler(button_callback_handler))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    print("BrainX Ultimate Quiz Pro Bot is running securely 24/7...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    
    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
