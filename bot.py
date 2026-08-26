import os
import logging
import asyncio
import aiohttp
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PollAnswerHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from aiohttp import web
import random

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle(request):
    return web.Response(text="BrainX Ultimate All-Exam AI PYQ Quiz Bot is live and running!")

async def start_web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

# ==================== HUGE ALL-EXAM PYQ QUESTION BANK ====================
SUBJECTS_DB = {
    "gk": [
        {"question": "[PYQ - UPSC/SSC] 'हंटर कमीशन' की रिपोर्ट में किसके विकास पर विशेष जोर दिया गया था?", "options": ["बालिका शिक्षा", "प्राथमिक शिक्षा", "उच्च शिक्षा", "तकनीकी शिक्षा"], "correct": 1, "explanation": "हंटर आयोग (1882) ने प्राथमिक शिक्षा के प्रसार और सुधार पर जोर दिया था।"},
        {"question": "[PYQ - UPPSC/REET] निम्नलिखित में से किस गवर्नर-जनरल ने भारत में ठगी प्रथा का अंत किया था?", "options": ["लॉर्ड कार्नवालिस", "लॉर्ड विलियम बेंटिक", "लॉर्ड डलहौजी", "लॉर्ड कर्जन"], "correct": 1, "explanation": "लॉर्ड विलियम बेंटिक ने कर्नल स्लीमैन की सहायता से ठगी प्रथा का दमन किया।"},
        {"question": "[PYQ - SSC CGL] सिंधु घाटी सभ्यता का कौन सा स्थल घग्गर नदी के किनारे स्थित था?", "options": ["लोथल", "कालीबंगा", "मोहनजोदड़ो", "हरप्पा"], "correct": 1, "explanation": "कालीबंगा घग्गर (सरस्वती) नदी के तट पर स्थित है।"},
        {"question": "[PYQ - SSC/UPSC] 'कर्क रेखा' भारत के कितने राज्यों से होकर गुजरती है?", "options": ["6", "7", "8", "9"], "correct": 2, "explanation": "कर्क रेखा भारत के 8 राज्यों से गुजरती है।"},
        {"question": "[PYQ - Geography] भारत की सबसे लंबी स्थलीय सीमा किस देश के साथ लगती है?", "options": ["चीन", "पाकिस्तान", "बांग्लादेश", "नेपाल"], "correct": 2, "explanation": "भारत की सबसे लंबी अंतरराष्ट्रीय सीमा बांग्लादेश के साथ है।"}
    ],
    "history": [
        {"question": "[PYQ - History] जैन धर्म के 24वें तीर्थंकर कौन थे?", "options": ["ऋषभदेव", "पार्श्वनाथ", "महावीर स्वामी", "अरिष्टनेमी"], "correct": 2, "explanation": "भगवान महावीर जैन धर्म के अंतिम व 24वें तीर्थंकर थे।"},
        {"question": "[PYQ - REET] राजस्थान में 'भगत आंदोलन' का नेतृत्व किसने किया था?", "options": ["गोविन्द गुरु", "मातृकुंडिया", "विजय सिंह पथिक", "जमुनालाल बजाज"], "correct": 0, "explanation": "गोविन्द गुरु ने संप सभा की स्थापना कर भीलों में भगत आंदोलन चलाया था।"},
        {"question": "[PYQ - History] 1857 की क्रांति की शुरुआत कहाँ से हुई थी?", "options": ["दिल्ली", "कानपूर", "मेरठ", "झाँसी"], "correct": 2, "explanation": "1857 के विद्रोह की शुरुआत 10 मई को मेरठ से हुई थी।"},
        {"question": "[PYQ - Ancient] 'अर्थशास्त्र' पुस्तक के लेखक कौन हैं?", "options": ["मेगस्थनीज", "चाणक्य", "कालिदास", "बाणभट्ट"], "correct": 1, "explanation": "अर्थशास्त्र चाणक्य (कौटिल्य) द्वारा लिखी गई थी।"}
    ],
    "polity": [
        {"question": "[PYQ - UPSC] भारतीय संविधान के किस अनुच्छेद के तहत राज्यों को 'ग्राम पंचायतों' के संगठन का निर्देश है?", "options": ["अनुच्छेद 36", "अनुच्छेद 40", "अनुच्छेद 48", "अनुच्छेद 51"], "correct": 1, "explanation": "अनुच्छेद 40 ग्राम पंचायतों के संगठन से संबंधित है।"},
        {"question": "[PYQ - SSC] लोकसभा और राज्यसभा की संयुक्त बैठक की अध्यक्षता कौन करता है?", "options": ["राष्ट्रपति", "राज्यसभा का सभापति", "लोकसभा अध्यक्ष", "प्रधानमंत्री"], "correct": 2, "explanation": "संयुक्त बैठक की अध्यक्षता लोकसभा अध्यक्ष करते हैं।"},
        {"question": "[PYQ - UPPSC] प्रस्तावना में 'समाजवादी' और 'धर्मनिरपेक्ष' शब्द किस संशोधन से जोड़े गए?", "options": ["42वें संशोधन", "44वें संशोधन", "86वें संशोधन", "73वें संशोधन"], "correct": 0, "explanation": "1976 के 42वें संविधान संशोधन द्वारा जोड़े गए।"},
        {"question": "[PYQ - Polity] भारत के महान्यायवादी (Attorney General) की नियुक्ति कौन करता है?", "options": ["प्रधानमंत्री", "राष्ट्रपति", "मुख्य न्यायाधीश", "लोकसभा अध्यक्ष"], "correct": 1, "explanation": "महान्यायवादी की नियुक्ति राष्ट्रपति द्वारा की जाती है।"}
    ],
    "science": [
        {"question": "[PYQ - RRB/SSC] मनुष्य के शरीर में 'लाल रक्त कणिकाओं' (RBC) का निर्माण कहाँ होता है?", "options": ["तल्ली (Spleen)", "यकृत (Liver)", "अस्थिमज्जा (Bone Marrow)", "हृदय (Heart)"], "correct": 2, "explanation": "RBC का निर्माण लाल अस्थिमज्जा में होता है।"},
        {"question": "[PYQ - Science] प्रकाश वर्ष (Light Year) किसका मात्रक है?", "options": ["समय", "दूरी", "प्रकाश तीव्रता", "वेग"], "correct": 1, "explanation": "प्रकाश वर्ष खगोलीय दूरियाँ मापने का मात्रक है।"},
        {"question": "[PYQ - Science] विटामिन C का रासायनिक नाम क्या है?", "options": ["साइट्रिक एसिड", "एस्कॉर्बिक एसिड", "थियामीन", "टोकोफेरॉल"], "correct": 1, "explanation": "विटामिन C का रासायनिक नाम एस्कॉर्बिक एसिड है।"}
    ],
    "pedagogy": [
        {"question": "[PYQ - UPTET/CTET] बाल मनोविज्ञान के अनुसार शिक्षा का केंद्र बिंदु क्या होता है?", "options": ["शिक्षक", "बालक (विद्यार्थी)", "विद्यालय", "पाठ्यक्रम"], "correct": 1, "explanation": "आधुनिक शिक्षा प्रणाली बाल-केंद्रित (Child-centric) है।"}
    ],
    "hindi_eng": [
        {"question": "[PYQ - UPTET] 'उद्घाटन' का सही संधि-विच्छेद क्या होगा?", "options": ["उत् + घाटन", "उद् + घाटन", "उत् + धाटन", "उद + घाटन"], "correct": 0, "explanation": "उत् + घाटन = उद्घाटन (व्यंजन संधि)।"},
        {"question": "[PYQ - SSC] Select the correct spelling:", "options": ["Lieutenant", "Leutinant", "Lietutenant", "Luitenant"], "correct": 0, "explanation": "Lieutenant की सही स्पेलिंग यही है।"},
        {"question": "[PYQ - Hindi] 'जो सब कुछ जानता हो' वाक्यांश के लिए एक शब्द क्या होगा?", "options": ["अल्पज्ञ", "सर्वज्ञ", "विद्वान", "ज्ञानी"], "correct": 1, "explanation": "सब कुछ जानने वाले को सर्वज्ञ कहते हैं।"},
        {"question": "[PYQ - English] What is the antonym of 'Abundant'?", "options": ["Scanty", "Plentiful", "Ample", "Generous"], "correct": 0, "explanation": "Abundant का विलोम Scanty होता है।"}
    ]
}

active_sessions = {}
ai_topic_state = {}

# ==================== AI QUESTION GENERATOR ====================
async def generate_ai_questions(topic: str, count: int = 10):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        return None

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Generate {count} high-level competitive exam multiple choice questions about '{topic}' in strict JSON format. "
        "Each object in the JSON array must have keys: 'question' (string in Hindi or English), "
        "'options' (list of 4 strings), 'correct' (integer index from 0 to 3), and 'explanation' (string). "
        "Do not include any markdown formatting like ```json in the output, just raw JSON."
    )

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=35) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    if content.startswith("```"):
                        content = content.split("```")[1]
                        if content.startswith("json"):
                            content = content[4:]
                    content = content.strip()
                    return json.loads(content)
    except Exception as e:
        logging.error(f"AI Generation Error: {e}")
    
    return None

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_sessions:
        active_sessions[chat_id]["active"] = False
        
    keyboard = [
        [
            InlineKeyboardButton("📚 सामान्य ज्ञान (GK)", callback_data="sub_gk"),
            InlineKeyboardButton("📜 इतिहास (History)", callback_data="sub_history"),
        ],
        [
            InlineKeyboardButton("⚖️ राजव्यवस्था (Polity)", callback_data="sub_polity"),
            InlineKeyboardButton("🔬 विज्ञान (Science)", callback_data="sub_science"),
        ],
        [
            InlineKeyboardButton("👶 शिक्षाशास्त्र (Pedagogy)", callback_data="sub_pedagogy"),
            InlineKeyboardButton("🔤 हिंदी & अंग्रेजी", callback_data="sub_hindi_eng"),
        ],
        [
            InlineKeyboardButton("🤖 AI से खुद नए प्रश्न बनाएँ", callback_data="sub_ai")
        ]
    ]
    await update.message.reply_text(
        f"🎯 **BrainX Ultimate PYQ & AI Master Bot** 🎯\n\n"
        f"👑 **Creator:** @krishnazxy\n\n"
        f"चरण 1: कृपया चुनें कि किस विषय या माध्यम से क्विज़ खेलनी है:\n\n"
        f"💡 *टिप: आप सीधे चैट में सवाल, ऑप्शन और सही नंबर भेजकर भी तुरंत पोल बना सकते हैं!*",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def subject_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    subject_key = query.data.split("_")[1]
    
    if subject_key == "ai":
        ai_topic_state[chat_id] = "waiting_for_topic"
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="🤖 **AI Quiz Mode:**\n\nकृपया चैट में किसी भी टॉपिक का नाम लिखकर भेजें जिस पर आप नए प्रश्न बनाना चाहते हैं (जैसे: `Rajasthan Geography` या `Indian Economy`):"
        )
        return

    active_sessions[chat_id] = {"subject": subject_key}
    await ask_question_count(chat_id, context, message_id, subject_key.upper())

async def ask_question_count(chat_id, context, message_id, title):
    keyboard = [
        [
            InlineKeyboardButton("5 प्रश्न", callback_data="cnt_5"),
            InlineKeyboardButton("10 प्रश्न", callback_data="cnt_10"),
            InlineKeyboardButton("15 प्रश्न", callback_data="cnt_15"),
        ],
        [
            InlineKeyboardButton("20 प्रश्न", callback_data="cnt_20"),
            InlineKeyboardButton("25 प्रश्न", callback_data="cnt_25"),
            InlineKeyboardButton("50 प्रश्न", callback_data="cnt_50"),
        ]
    ]
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"✅ विषय/मोड चुना गया: **{title}**\n\n"
             f"चरण 2: अब चुनें कि आप **कितने प्रश्नों का सेट** खेलना चाहते हैं?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# टेक्स्ट मैसेज और इंस्टेंट पोल मेकर + AI टॉपिक हैंडलर
async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    # 1. AI टॉपिक का इंतज़ार कर रहा हो
    if chat_id in ai_topic_state and ai_topic_state[chat_id] == "waiting_for_topic":
        topic = text.strip()
        del ai_topic_state[chat_id]
        
        active_sessions[chat_id] = {"subject": "ai", "ai_topic": topic}
        
        keyboard = [
            [
                InlineKeyboardButton("5 प्रश्न", callback_data="cnt_5"),
                InlineKeyboardButton("10 प्रश्न", callback_data="cnt_10"),
                InlineKeyboardButton("15 प्रश्न", callback_data="cnt_15"),
            ],
            [
                InlineKeyboardButton("20 प्रश्न", callback_data="cnt_20"),
                InlineKeyboardButton("25 प्रश्न", callback_data="cnt_25"),
            ]
        ]
        await update.message.reply_text(
            f"✅ AI टॉपिक सेट हुआ: **{topic}**\n\n"
            f"चरण 2: अब चुनें कि AI से कितने प्रश्न तैयार करवाने हैं?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    # 2. इंस्टेंट पोल मेकर (मैसेज भेजते ही पोल बनाना)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if len(lines) >= 3 and chat_id not in active_sessions.get(chat_id, {}):
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

async def count_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    count_val = int(query.data.split("_")[1])
    if chat_id not in active_sessions:
        active_sessions[chat_id] = {}
    active_sessions[chat_id]["count"] = count_val
    
    keyboard = [
        [
            InlineKeyboardButton("⚡ 10s प्रति प्रश्न", callback_data="t_10"),
            InlineKeyboardButton("⏱️ 15s प्रति प्रश्न", callback_data="t_15"),
            InlineKeyboardButton("🧠 20s प्रति प्रश्न", callback_data="t_20"),
        ]
    ]
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=f"✅ प्रश्न संख्या: **{count_val} प्रश्न** सेट हो गए।\n\n"
             f"चरण 3: प्रति प्रश्न के लिए **समय (Timer)** चुनें:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def timer_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    
    timer_val = int(query.data.split("_")[1])
    session_data = active_sessions.get(chat_id, {})
    subject_key = session_data.get("subject", "gk")
    count_val = session_data.get("count", 10)
    
    if subject_key == "ai":
        topic = session_data.get("ai_topic", "General Studies")
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"🤖 **AI '{topic}' पर {count_val} नए प्रश्न तैयार कर रहा है...** कृपया थोड़ा इंतज़ार करें।"
        )
        
        selected_questions = await generate_ai_questions(topic, count=count_val)
        if not selected_questions or not isinstance(selected_questions, list):
            await context.bot.send_message(chat_id, "❌ AI प्रश्न जनरेट करने में असफल रहा। कृपया /start से दोबारा प्रयास करें।")
            return
        quiz_name = f"AI Quiz: {topic}"
    else:
        available_qs = SUBJECTS_DB.get(subject_key, SUBJECTS_DB["gk"])
        selected_questions = random.sample(available_qs, min(count_val, len(available_qs)))
        quiz_name = f"{subject_key.upper()} PYQ Set"
        
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"🚀 **{quiz_name} शुरू हो चुकी है!**\n📊 कुल प्रश्न: {len(selected_questions)} | ⏱️ टाइमर: {timer_val}s\n\nपहला प्रश्न आ रहा है..."
        )

    active_sessions[chat_id] = {
        "questions": selected_questions,
        "quiz_name": quiz_name,
        "current_q": 0,
        "scores": {},
        "timer": timer_val,
        "active": True
    }
    
    await asyncio.sleep(1)
    await send_next_question(chat_id, context)

async def send_next_question(chat_id, context):
    game = active_sessions.get(chat_id)
    if not game or not game["active"]:
        return

    q_idx = game["current_q"]
    q_list = game["questions"]
    timer = game["timer"]
    
    if q_idx >= len(q_list):
        if game["active"]:
            game["active"] = False
            await show_final_leaderboard(chat_id, context)
        return

    q_data = q_list[q_idx]
    
    try:
        await context.bot.send_poll(
            chat_id=chat_id,
            question=f"[{game['quiz_name']}] प्रश्न {q_idx + 1} / {len(q_list)}:\n{q_data['question']}",
            options=q_data["options"],
            type="quiz",
            correct_option_id=q_data["correct"],
            is_anonymous=False,
            explanation=q_data.get("explanation", "सही उत्तर चुनें!"),
            open_period=timer
        )
        
        game["current_q"] += 1
        
        for _ in range(timer + 1):
            await asyncio.sleep(1)
            if chat_id not in active_sessions or not active_sessions[chat_id]["active"]:
                return

        if chat_id in active_sessions and active_sessions[chat_id]["active"]:
            await send_next_question(chat_id, context)
            
    except Exception as e:
        logging.error(f"Error sending poll: {e}")

async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    user = answer.user
    user_id = user.id
    user_name = user.first_name if user.first_name else "Khiladi"
    selected_options = answer.option_ids

    for chat_id, game in active_sessions.items():
        if game["active"]:
            q_idx = game["current_q"] - 1
            q_list = game["questions"]

            if 0 <= q_idx < len(q_list):
                correct_opt = q_list[q_idx]["correct"]
                if user_id not in game["scores"]:
                    game["scores"][user_id] = {"name": user_name, "score": 0}

                if correct_opt in selected_options:
                    game["scores"][user_id]["score"] += 1
            break

async def stop_quiz_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in active_sessions and active_sessions[chat_id]["active"]:
        active_sessions[chat_id]["active"] = False
        await update.message.reply_text("🛑 **क्विज़ को तुरंत रोक दिया गया है!**")
        await show_final_leaderboard(chat_id, context)
    else:
        await update.message.reply_text("⚠️ इस समय कोई क्विज़ सक्रिय नहीं है।")

async def show_final_leaderboard(chat_id, context):
    if chat_id not in active_sessions:
        return
        
    game = active_sessions[chat_id]
    game["active"] = False
    scores_dict = game["scores"]
    quiz_name = game["quiz_name"]
    total_qs = len(game["questions"])

    report = f"🏆 **====================** 🏆\n"
    report += f"   🌟 **{quiz_name.upper()} LEADERBOARD** 🌟\n"
    report += f"🏆 **====================** 🏆\n\n"

    report += f"👑 **Bot Developed & Created By:** @krishnazxy 🚀\n\n"

    if not scores_dict:
        report += "🏁 क्विज़ समाप्त! किसी ने उत्तर दर्ज नहीं किया।\n"
    else:
        sorted_players = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)
        first_winner = sorted_players[0]

        report += f"🎉 **चैंपियन विनर:** {first_winner['name']} (स्कोर: {first_winner['score']}/{total_qs}) 🥇\n\n"
        report += "📜 **सभी खिलाड़ियों की स्कोरलिस्ट:**\n"
        report += "----------------------------------------\n"
        for idx, player in enumerate(sorted_players, start=1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
            report += f"{medal} **{player['name']}** — {player['score']} Points\n"
        report += "----------------------------------------\n"

    report += "💖 *शानदार प्रयास! अपनी तैयारी जारी रखें।* ✨"
    await context.bot.send_message(chat_id=chat_id, text=report)
    if chat_id in active_sessions:
        del active_sessions[chat_id]

async def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return

    await start_web_server()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stopquiz", stop_quiz_cmd))
    app.add_handler(CallbackQueryHandler(subject_callback_handler, pattern="^sub_"))
    app.add_handler(CallbackQueryHandler(count_callback_handler, pattern="^cnt_"))
    app.add_handler(CallbackQueryHandler(timer_callback_handler, pattern="^t_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    print("BrainX Ultimate All-Exam AI PYQ Master Bot is running...")
    
    app.initialize()
    app.start()
    app.updater.start_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
    
    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
