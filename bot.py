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
from aiohttp import web

# लॉगिंग सेट अप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render के लिए Web Server
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

# ==================== FULL QUESTION BANKS ====================

# 50 GK PYQ (हिंदी में)
GK_QUESTIONS = [
    {"question": "भारत का राष्ट्रीय गीत 'वंदे मातरम' किसने लिखा है?", "options": ["बंकिम चंद्र चट्टोपाध्याय", "रविंद्रनाथ टैगोर", "इक़बाल", "सरदार पटेल"], "correct": 0, "explanation": "वंदे मातरम बंकिम चंद्र चट्टोपाध्याय द्वारा आनंदमठ से लिया गया है।"},
    {"question": "भारत का संविधान कब लागू हुआ?", "options": ["15 अगस्त 1947", "26 जनवरी 1950", "26 नवंबर 1949", "2 अक्टूबर 1952"], "correct": 1, "explanation": "भारत का संविधान 26 जनवरी 1950 को पूर्ण रूप से लागू हुआ था।"},
    {"question": "महात्मा गांधी ने असहयोग आंदोलन किस वर्ष शुरू किया था?", "options": ["1920", "1922", "1930", "1942"], "correct": 0, "explanation": "असहयोग आंदोलन की शुरुआत 1920 में महात्मा गांधी ने की थी।"},
    {"question": "भारत में सबसे लंबी नदी कौन सी है?", "options": ["यमुना", "ब्रह्मपुत्र", "गंगा", "गोदावरी"], "correct": 2, "explanation": "गंगा भारत की सबसे लंबी नदी है।"},
    {"question": "किस ग्रह को 'लाल ग्रह' कहा जाता है?", "options": ["शुक्र", "मंगल", "बुध", "शनि"], "correct": 1, "explanation": "आयरन ऑक्साइड की अधिकता के कारण मंगल ग्रह को लाल ग्रह कहते हैं।"},
    {"question": "भारत के प्रथम प्रधानमंत्री कौन थे?", "options": ["डॉ. राजेंद्र प्रसाद", "जवाहरलाल नेहरू", "वल्लभभाई पटेल", "लाल बहादुर शास्त्री"], "correct": 1, "explanation": "पंडित जवाहरलाल नेहरू भारत के प्रथम प्रधानमंत्री थे।"},
    {"question": "कंप्यूटर का आविष्कार किसने किया था?", "options": ["चार्ल्स बेबेज", "अल्बर्ट आइंस्टीन", "थॉमस एडिसन", "आइज़ैक न्यूटन"], "correct": 0, "explanation": "चार्ल्स बेबेज को कंप्यूटर का जनक कहा जाता है।"},
    {"question": "राष्ट्रीय विज्ञान दिवस कब मनाया जाता है?", "options": ["28 फरवरी", "5 शिक्षक", "15 अगस्त", "26 जनवरी"], "correct": 0, "explanation": "28 फरवरी को राष्ट्रीय विज्ञान दिवस मनाया जाता है।"},
    {"question": "भारत का राष्ट्रीय पशु क्या है?", "options": ["शेर", "हाथी", "बाघ", "चीता"], "correct": 2, "explanation": "भारत का राष्ट्रीय पशु बाघ (Tiger) है।"},
    {"question": "क्षेत्रफल की दृष्टि से भारत का सबसे बड़ा राज्य कौन सा है?", "options": ["महाराष्ट्र", "उत्तर प्रदेश", "राजस्थान", "मध्य प्रदेश"], "correct": 2, "explanation": "क्षेत्रफल की दृष्टि से राजस्थान सबसे बड़ा राज्य है।"},
    {"question": "भारत का सबसे छोटा राज्य कौन सा है?", "options": ["गोवा", "सिक्किम", "त्रिपुरा", "मिजोरम"], "correct": 0, "explanation": "गोवा क्षेत्रफल की दृष्टि से भारत का सबसे छोटा राज्य है।"},
    {"question": "भारतीय मरुस्थल का क्या नाम है?", "options": ["थार", "सहारा", "गोबी", "कालाहारी"], "correct": 0, "explanation": "भारत के पश्चिमी भाग में थार का मरुस्थल स्थित है।"},
    {"question": "पृथ्वी का एकमात्र प्राकृतिक उपग्रह कौन सा है?", "options": ["मंगल", "चंद्रमा", "टाइटन", "फोबॉस"], "correct": 1, "explanation": "चंद्रमा पृथ्वी का एकमात्र प्राकृतिक उपग्रह है।"},
    {"question": "बिहू किस राज्य का प्रसिद्ध लोक नृत्य है?", "options": ["असम", "पंजाब", "केरल", "गुजरात"], "correct": 0, "explanation": "बिहू असम राज्य का प्रसिद्ध लोक नृत्य है।"},
    {"question": "पोंगल किस राज्य का प्रमुख त्यौहार है?", "options": ["तमिलनाडु", "केरल", "कर्नाटक", "आंध्र प्रदेश"], "correct": 0, "explanation": "पोंगल तमिलनाडु का प्रमुख फसल उत्सव है।"},
    {"question": "टेलीविजन का आविष्कार किसने किया था?", "options": ["जे. एल. बेयरड", "ग्राहम बेल", "मार्कोनी", "एडिसन"], "correct": 0, "explanation": "जे. एल. बेयरड ने टेलीविजन का आविष्कार किया था।"},
    {"question": "भारत की पहली महिला प्रधानमंत्री कौन थीं?", "options": ["प्रतिभा पाटिल", "सरोजिनी नायडू", "इंदिरा गांधी", "सुचेता कृपलानी"], "correct": 2, "explanation": "इंदिरा गांधी भारत की पहली महिला प्रधानमंत्री थीं।"},
    {"question": "इंकलाब जिंदाबाद का नारा किसने दिया था?", "options": ["भगत सिंह", "सुभाष चंद्र बोस", "महात्मा गांधी", "चंद्रशेखर आजाद"], "correct": 0, "explanation": "इंकलाब जिंदाबाद का नारा भगत सिंह ने लोकप्रिय किया था।"},
    {"question": "जलियांवाला बाग हत्याकांड कहाँ हुआ था?", "options": ["अमृतसर", "लाहौर", "दिल्ली", "मेरठ"], "correct": 0, "explanation": "जलियांवाला बाग हत्याकांड 13 अप्रैल 1919 को अमृतसर में हुआ था।"},
    {"question": "भारत की राजधानी नई दिल्ली कब बनी थी?", "options": ["1911", "1947", "1950", "1930"], "correct": 0, "explanation": "1911 में दिल्ली दरबार में राजधानी परिवर्तन की घोषणा हुई थी।"},
    {"question": "सवा लक्षित 'ओणम' त्यौहार कहाँ मनाया जाता है?", "options": ["केरल", "तमिलनाडु", "असम", "गोवा"], "correct": 0, "explanation": "ओणम केरल का प्रमुख सांस्कृतिक त्यौहार है।"},
    {"question": "भारत के किस राज्य में सबसे पहले सूर्य निकलता है?", "options": ["अरुणाचल प्रदेश", "गुजरात", "असम", "नागालैंड"], "correct": 0, "explanation": "अरुणाचल प्रदेश में भारत में सबसे पहले सूर्योदय होता है।"},
    {"question": "बुद्ध ने अपना पहला उपदेश कहाँ दिया था?", "options": ["सारनाथ", "बोधगया", "कुशीनगर", "लुंबिनी"], "correct": 0, "explanation": "महात्मा बुद्ध ने सारनाथ में अपना पहला उपदेश दिया था।"},
    {"question": "हवा महल कहाँ स्थित है?", "options": ["जयपुर", "उदयपुर", "जोधपुर", "दिल्ली"], "correct": 0, "explanation": "प्रसिद्ध हवा महल जयपुर (राजस्थान) में स्थित है।"},
    {"question": "लौह पुरुष के नाम से किसे जाना जाता है?", "options": ["सरदार वल्लभभाई पटेल", "महात्मा गांधी", "जवाहरलाल नेहरू", "बाल गंगाधर तिलक"], "correct": 0, "explanation": "सरदार पटेल को भारत का लौह पुरुष कहा जाता है।"},
    {"question": "वेदों की ओर लौटो का नारा किसने दिया था?", "options": ["स्वामी दयानंद सरस्वती", "स्वामी विवेकानंद", "राजा राममोहन राय", "तुलसीदास"], "correct": 0, "explanation": "स्वामी दयानंद सरस्वती ने वेदों की ओर लौटो का नारा दिया था।"},
    {"question": "भारत का राष्ट्रीय पक्षी कौन सा है?", "options": ["मोर", "तोता", "कौवा", "हंस"], "correct": 0, "explanation": "भारत का राष्ट्रीय पक्षी मोर (Peacock) है।"},
    {"question": "अंतरिक्ष में जाने वाले पहले भारतीय कौन थे?", "options": ["राकेश शर्मा", "रविश मल्होत्रा", "कल्पना चावला", "सुनीता विलियम्स"], "correct": 0, "explanation": "स्क्वाड्रन लीडर राकेश शर्मा अंतरिक्ष में जाने वाले पहले भारतीय थे।"},
    {"question": "भारत की प्रथम महिला मुख्यमंत्री कौन थीं?", "options": ["सुचेता कृपलानी", "सरोजिनी नायडू", "मायावती", "ममता बनर्जी"], "correct": 0, "explanation": "सुचेता कृपलानी उत्तर प्रदेश की पहली महिला मुख्यमंत्री थीं।"},
    {"question": "संयुक्त राष्ट्र संघ (UN) का मुख्यालय कहाँ है?", "options": ["न्यूयार्क", "जेनेवा", "पेरिस", "लंदन"], "correct": 0, "explanation": "संयुक्त राष्ट्र संघ का मुख्यालय न्यूयॉर्क, यूएसए में है।"},
    {"question": "अंतरराष्ट्रीय महिला दिवस कब मनाया जाता है?", "options": ["8 मार्च", "5 सितंबर", "14 नवंबर", "1 दिसंबर"], "correct": 0, "explanation": "प्रतिवर्ष 8 मार्च को अंतरराष्ट्रीय महिला दिवस मनाया जाता है।"},
    {"question": "घेઘ रोग किसकी कमी से होता है?", "options": ["आयोडीन", "विटामिन सी", "कैल्शियम", "आयरन"], "correct": 0, "explanation": "शरीर में आयोडीन की कमी से घेंघा (Goitre) रोग होता है।"},
    {"question": "विटामिन बी की कमी से कौन सा रोग होता है?", "options": ["बेरी-बेरी", "स्कर्वी", "रिकेट्स", "रतौंधी"], "correct": 0, "explanation": "विटामिन B1 (थियामीन) की कमी से बेरी-बेरी रोग होता है।"},
    {"question": "विटामिन सी की कमी से कौन सी बीमारी होती है?", "options": ["स्कर्वी", "बेरी-बेरी", "रिकेट्स", "एनीमिया"], "correct": 0, "explanation": "विटामिन C की कमी से मसूड़ों में स्कर्वी रोग होता है।"},
    {"question": "दूध में कौन सा विटामिन नहीं पाया जाता है?", "options": ["विटामिन सी", "विटामिन ए", "विटामिन डी", "विटामिन बी"], "correct": 0, "explanation": "दूध में विटामिन C नहीं पाया जाता है।"},
    {"question": "किस विटामिन की कमी से खून का थक्का नहीं जमता?", "options": ["विटामिन के", "विटामिन ई", "विटामिन डी", "विटामिन ए"], "correct": 0, "explanation": "विटामिन K की कमी से रक्त का थक्का जमना बंद हो जाता है।"},
    {"question": "प्रकाश वर्ष किसका मात्रक है?", "options": ["दूरी", "समय", "प्रकाश तीव्रता", "द्रव्यमान"], "correct": 0, "explanation": "प्रकाश वर्ष खगोलीय दूरी मापने की इकाई है।"},
    {"question": "स्वर्ण मंदिर कहाँ स्थित है?", "options": ["अमृतसर", "जालंधर", "चंडीगढ़", "लुधियाना"], "correct": 0, "explanation": "प्रसिद्ध स्वर्ण मंदिर अमृतसर (पंजाब) में स्थित है।"},
    {"question": "चारमीनार कहाँ स्थित है?", "options": ["हैदराबाद", "दिल्ली", "आगरा", "सिकंदराबाद"], "correct": 0, "explanation": "चारमीनार हैदराबाद (तेलंगाना) में स्थित है।"},
    {"question": "कुतुब मीनार कहाँ स्थित है?", "options": ["दिल्ली", "आगरा", "मुंबई", "जयपुर"], "correct": 0, "explanation": "कुतुब मीनार नई दिल्ली में स्थित है।"},
    {"question": "गेटवे ऑफ़ इंडिया कहाँ स्थित है?", "options": ["मुंबई", "दिल्ली", "कोलकाता", "चेन्नई"], "correct": 0, "explanation": "गेटवे ऑफ़ इंडिया मुंबई में स्थित है।"},
    {"question": "इंडिया गेट कहाँ स्थित है?", "options": ["नई दिल्ली", "मुंबई", "कोलकाता", "बेंगलुरु"], "correct": 0, "explanation": "इंडिया गेट नई दिल्ली में स्थित है।"},
    {"question": "ताजमहल किस नदी के किनारे स्थित है?", "options": ["यमुना", "गंगा", "ब्रह्मपुत्र", "चंबल"], "correct": 0, "explanation": "ताजमहल यमुना नदी के तट पर आगरा में स्थित है।"},
    {"question": "भारत का राष्ट्रीय खेल कौन सा है?", "options": ["हॉकी", "क्रिकेट", "कबड्डी", "फुटबॉल"], "correct": 0, "explanation": "भारत का पारंपरिक राष्ट्रीय खेल हॉकी माना जाता है।"},
    {"question": "शक संवत की शुरुआत किसने की थी?", "options": ["कनिष्क", "अशोक", "विक्रमादित्य", "समुद्रगुप्त"], "correct": 0, "explanation": "शक संवत की शुरुआत कनिष्क ने 78 ईस्वी में की थी।"},
    {"question": "भारत में सबसे पहले रेल कहाँ से कहाँ तक चली थी?", "options": ["मुंबई से ठाणे", "हावड़ा से हुगली", "चेन्नई से मदुरै", "दिल्ली से आगरा"], "correct": 0, "explanation": "भारत की पहली ट्रेन 1853 में मुंबई से ठाणे के बीच चली थी।"},
    {"question": "भारतीय राष्ट्रीय कांग्रेस की स्थापना कब हुई थी?", "options": ["1885", "1905", "1919", "1942"], "correct": 0, "explanation": "भारतीय राष्ट्रीय कांग्रेस की स्थापना 28 दिसंबर 1885 को हुई थी।"},
    {"question": "स्वतंत्र भारत के पहले गवर्नर जनरल कौन थे?", "options": ["लॉर्ड माउंटबेटन", "सी. राजगोपालाचारी", "डॉ. राजेंद्र प्रसाद", "जवाहरलाल नेहरू"], "correct": 0, "explanation": "स्वतंत्र भारत के पहले स्वतंत्र गवर्नर जनरल लॉर्ड माउंटबेटन थे।"},
    {"question": "संविधान सभा के स्थायी अध्यक्ष कौन थे?", "options": ["डॉ. राजेंद्र प्रसाद", "डॉ. भीमराव अंबेडकर", "सच्चिदानंद सिन्हा", "जवाहरलाल नेहरू"], "correct": 0, "explanation": "डॉ. राजेंद्र प्रसाद संविधान सभा के स्थायी अध्यक्ष चुने गए थे।"},
    {"question": "क्षेत्रफल की दृष्टि से भारत का विश्व में कौन सा स्थान है?", "options": ["सातवाँ", "पाँचवाँ", "छठा", "आठवाँ"], "correct": 0, "explanation": "क्षेत्रफल के मामले में भारत दुनिया का सातवां सबसे बड़ा देश है।"}
]

# 30 Hindi Questions
HINDI_QUESTIONS = [
    {"question": "'विद्यालय' शब्द का सही संधि विच्छेद क्या है?", "options": ["विद्या + आलय", "विध + आलय", "विद्य + लय", "विद्या + लय"], "correct": 0, "explanation": "विद्यालय दीर्घ स्वर संधि का उदाहरण है।"},
    {"question": "हिंदी वर्णमाला में कुल कितने स्वर होते हैं?", "options": ["10", "11", "13", "12"], "correct": 1, "explanation": "मानक हिंदी वर्णमाला में कुल 11 स्वर होते हैं।"},
    {"question": "'कमल' का पर्यायवाची शब्द इनमें से कौन सा है?", "options": ["जलद", "पंकज", "नीरद", "वारिधि"], "correct": 1, "explanation": "पंकज कमल का पर्यायवाची है।"},
    {"question": "जिसकी कोई उपमा न हो, उसे क्या कहते हैं?", "options": ["अनुपम", "अद्भुत", "सुंदर", "अद्वितीय"], "correct": 0, "explanation": "जिसकी कोई उपमा न हो उसे अनुपम कहते हैं।"},
    {"question": "'घोड़ा' का बहुवचन रूप क्या होगा?", "options": ["घोड़ें", "घोड़े", "घोड़ो", "घोड़ी"], "correct": 1, "explanation": "घोड़ा का बहुवचन 'घोड़े' होता है।"},
    {"question": "'सूर्य' का स्त्रीलिंग रूप क्या होगा?", "options": ["सूर्या", "सूर्यानी", "सूरज", "कोई नहीं"], "correct": 0, "explanation": "सूर्य का रूप सूर्या प्रयोग होता है।"},
    {"question": "हिंदी भाषा किस लिपि में लिखी जाती है?", "options": ["रोमन", "देवनागरी", "गुरुमुखी", "ब्राह्मी"], "correct": 1, "explanation": "हिंदी देवनागरी लिपि में लिखी जाती है।"},
    {"question": "'य, र, ल, व' किस प्रकार के व्यंजन हैं?", "options": ["उष्म व्यंजन", "अंतःस्थ व्यंजन", "स्पर्श व्यंजन", "संयुक्त व्यंजन"], "correct": 1, "explanation": "य, र, ल, व अंतःस्थ व्यंजन कहलाते हैं।"},
    {"question": "'महेश' का संधि विच्छेद क्या होगा?", "options": ["महा + ईश", "मही + श", "महान + ईश", "महा + श"], "correct": 0, "explanation": "महा + ईश = महेश (गुण स्वर संधि)।"},
    {"question": "अज्ञान में कौन सा उपसर्ग लगा है?", "options": ["अ", "ज्ञा", "ज्ञान", "अज्ञ"], "correct": 0, "explanation": "अज्ञान शब्द में 'अ' उपसर्ग है।"},
    {"question": "बुढ़ापा किस प्रकार की संज्ञा है?", "options": ["व्यक्तिवाचक", "जातिवाचक", "भाववाचक", "समूहवाचक"], "correct": 2, "explanation": "बुढ़ापा एक अवस्था है जो भाववाचक संज्ञा है।"},
    {"question": "जो सब कुछ जानता हो, उसे क्या कहते हैं?", "options": ["अल्पज्ञ", "सर्वज्ञ", "विद्वान", "ज्ञानी"], "correct": 1, "explanation": "जो सब कुछ जानता हो उसे सर्वज्ञ कहते हैं।"},
    {"question": "'आँखों का तारा होना' मुहावरे का अर्थ है?", "options": ["बहुत प्रिय होना", "धोखा देना", "आँख में दर्द होना", "क्रोध करना"], "correct": 0, "explanation": "आँखों का तारा होना यानी बहुत प्यारा होना।"},
    {"question": "'पाप-पुण्य' में कौन सा समास है?", "options": ["द्वंद्व समास", "तत्पुरुष समास", "कर्मधारय समास", "बहुव्रीहि समास"], "correct": 0, "explanation": "जिसमें दोनों पद प्रधान हों वहाँ द्वंद्व समास होता है।"},
    {"question": "शुद्ध वर्तनी का चयन कीजिए:", "options": ["उज्जवल", "उज्वल", "उज्जवल", "उज्जल"], "correct": 0, "explanation": "उज्जवल की शुद्ध वर्तनी में दोनों 'ज' आधे होते हैं।"},
    {"question": "राष्ट्रभाषा किसे कहते हैं?", "options": ["सरकारी कामकाज की भाषा", "बहुसंख्यक लोगों द्वारा बोली जाने वाली भाषा", "अंग्रेजी भाषा", "विदेशी भाषा"], "correct": 1, "explanation": "देश के अधिकांश लोगों द्वारा बोली जाने वाली भाषा राष्ट्रभाषा होती है।"},
    {"question": "'नयन' का सही संधि विच्छेद क्या है?", "options": ["ने + अन", "नै + अन", "नी + अन", "न + यन"], "correct": 0, "explanation": "ने + अन = नयन (अयादि संधि)।"},
    {"question": "'तीर्थयात्रा' में कौन सा समास है?", "options": ["तत्पुरुष समास", "अव्ययीभाव समास", "द्वंद्व समास", "कर्मधारय समास"], "correct": 0, "explanation": "तीर्थ की यात्रा - तत्पुरुष समास।"},
    {"question": "जिसकी गिनती न की जा सके, उसे क्या कहते हैं?", "options": ["गणनीय", "अगणनीय", "अमर", "अमित"], "correct": 1, "explanation": "जिसकी गिनती न हो सके उसे अगणनीय या अनगिनत कहते हैं।"},
    {"question": "'मित्रता' किस प्रकार की संज्ञा है?", "options": ["जातिवाचक", "भाववाचक", "व्यक्तिवाचक", "द्रव्यवाचक"], "correct": 1, "explanation": "मित्रता भाववाचक संज्ञा का उदाहरण है।"},
    {"question": "जिसका कोई शत्रु न हो, उसे क्या कहते हैं?", "options": ["अजातशत्रु", "मित्रहीन", "निर्दोष", "अजय"], "correct": 0, "explanation": "जिसका कोई शत्रु पैदा न हुआ हो उसे अजातशत्रु कहते हैं।"},
    {"question": "'हवा' का पर्यायवाची शब्द इनमें से कौन सा है?", "options": ["अनिल", "नल", "पावक", "अनल"], "correct": 0, "explanation": "अनिल हवा का पर्यायवाची है (अनल आग का है)।"},
    {"question": "हिंदी दिवस कब मनाया जाता है?", "options": ["14 सितंबर", "5 सितंबर", "26 जनवरी", "15 अगस्त"], "correct": 0, "explanation": "प्रतिवर्ष 14 सितंबर को हिंदी दिवस मनाया जाता है।"},
    {"question": "कारक के कुल कितने भेद होते हैं?", "options": ["6", "7", "8", "5"], "correct": 2, "explanation": "हिंदी व्याकरण में कारक के 8 भेद होते हैं।"},
    {"question": "सर्वनाम के कुल कितने भेद होते हैं?", "options": ["4", "5", "6", "7"], "correct": 2, "explanation": "सर्वनाम के कुल 6 भेद होते हैं।"},
    {"question": "विशेषण की कितनी अवस्थाएं होती हैं?", "options": ["2", "3", "4", "5"], "correct": 1, "explanation": "विशेषण की तीन अवस्थाएं होती हैं (मूलावस्था, उत्तरावस्था, उत्तमावस्था)।"},
    {"question": "'दूध का जला छाछ भी फूँक-फूँक कर पीता है' लोकोक्ति का अर्थ है?", "options": ["सावधानी बरतना", "जल जाना", "दूध पसंद न आना", "डर जाना"], "correct": 0, "explanation": "एक बार धोखा खाने के बाद व्यक्ति हमेशा सतर्क रहता है।"},
    {"question": "'अकबरनामा' किस भाषा में लिखा गया ग्रंथ है?", "options": ["फारसी", "अरबी", "हिंदी", "उर्दू"], "correct": 0, "explanation": "अकबरनामा फारसी भाषा में लिखा गया है।"},
    {"question": "श और ष का उच्चारण स्थान क्या है?", "options": ["तालू और मूर्धा", "कंठ", "दन्त", "ओष्ठ"], "correct": 0, "explanation": "'श' तालव्य है और 'ष' मूर्धन्य है।"},
    {"question": "भाषा की सबसे छोटी इकाई क्या है?", "options": ["शब्द", "वर्ण या ध्वनि", "वाक्य", "पद"], "correct": 1, "explanation": "वर्ण या ध्वनि भाषा की सबसे छोटी इकाई है।"}
]

# 20 English Questions
ENGLISH_QUESTIONS = [
    {"question": "What is the antonym of 'Brave'?", "options": ["Coward", "Bold", "Fearless", "Courageous"], "correct": 0, "explanation": "Coward is the opposite (antonym) of brave."},
    {"question": "Choose the correct spelling:", "options": ["Recieve", "Receive", "Riciive", "Receeve"], "correct": 1, "explanation": "The correct spelling is Receive."},
    {"question": "He ___ to school every day. (Fill in the blank)", "options": ["go", "gone", "goes", "going"], "correct": 2, "explanation": "With singular third-person 'He', we use 'goes'."},
    {"question": "What is the synonym of 'Happy'?", "options": ["Sad", "Joyful", "Angry", "Tired"], "correct": 1, "explanation": "Joyful has a similar meaning to happy."},
    {"question": "Identify the noun in the sentence: 'The cat slept on the mat.'", "options": ["Slept", "On", "Cat", "The"], "correct": 2, "explanation": "'Cat' is a noun in the sentence."},
    {"question": "What is the past tense of 'Run'?", "options": ["Runned", "Ran", "Running", "Runs"], "correct": 1, "explanation": "The past tense of run is ran."},
    {"question": "Which article is used before a vowel sound?", "options": ["A", "An", "The", "None"], "correct": 1, "explanation": "'An' is used before words starting with vowel sounds."},
    {"question": "What is the plural form of 'Child'?", "options": ["Childs", "Children", "Childes", "Childrens"], "correct": 1, "explanation": "The plural of child is children."},
    {"question": "Choose the correct preposition: 'He is sitting ___ the chair.'", "options": ["in", "on", "at", "by"], "correct": 1, "explanation": "We use 'on' for surfaces like chairs."},
    {"question": "What is the antonym of 'Hot'?", "options": ["Cold", "Warm", "Cool", "Boiling"], "correct": 0, "explanation": "Cold is the opposite of hot."},
    {"question": "Select the adjective in: 'She has a beautiful dress.'", "options": ["She", "Has", "Beautiful", "Dress"], "correct": 2, "explanation": "'Beautiful' describes the dress, so it's an adjective."},
    {"question": "What is the synonym of 'Quick'?", "options": ["Slow", "Fast", "Late", "Heavy"], "correct": 1, "explanation": "Fast means quick."},
    {"question": "Which of these is a pronoun?", "options": ["Apple", "He", "Run", "Slowly"], "correct": 1, "explanation": "'He' is a personal pronoun."},
    {"question": "What is the past participle of 'Eat'?", "options": ["Ate", "Eaten", "Eating", "Eats"], "correct": 1, "explanation": "The past participle of eat is eaten."},
    {"question": "Choose the correct spelling:", "options": ["Necessary", "Nessary", "Neccesary", "Necassary"], "correct": 0, "explanation": "Necessary is spelled with one c and two s's."},
    {"question": "What is the antonym of 'Strong'?", "options": ["Powerful", "Weak", "Sturdy", "Tough"], "correct": 1, "explanation": "Weak is the antonym of strong."},
    {"question": "Identify the verb: 'Birds fly in the sky.'", "options": ["Birds", "Fly", "Sky", "In"], "correct": 1, "explanation": "'Fly' is the action verb."},
    {"question": "What is the feminine gender of 'Lion'?", "options": ["Lioness", "Lion", "Tiger", "Cub"], "correct": 0, "explanation": "The feminine of lion is lioness."},
    {"question": "Which word means the same as 'Big'?", "options": ["Small", "Tiny", "Large", "Short"], "correct": 2, "explanation": "Large is a synonym for big."},
    {"question": "Complete the sentence: 'She is singing ___ song.'", "options": ["a", "an", "the", "none"], "correct": 0, "explanation": "'A song' is grammatically correct here."}
]

# 50 Art & Culture Questions
ART_QUESTIONS = [
    {"question": "ताजमहल का डिजाइन किसने तैयार किया था?", "options": ["उस्ताद अहमद लाहौरी", "उस्ताद ईसा", "शाहजहाँ", "बीरबल"], "correct": 0, "explanation": "ताजमहल के मुख्य वास्तुकार उस्ताद अहमद लाहौरी थे।"},
    {"question": "कथकली नृत्य किस राज्य से संबंधित है?", "options": ["उत्तर प्रदेश", "केरल", "तमिलनाडु", "आंध्र प्रदेश"], "correct": 1, "explanation": "कथकली केरल का प्रमुख शास्त्रीय नृत्य है।"},
    {"question": "कोणार्क का सूर्य मंदिर किस राज्य में स्थित है?", "options": ["उड़ीसा", "कर्नाटक", "राजस्थान", "गुजरात"], "correct": 0, "explanation": "कोणार्क का सूर्य मंदिर ओडिशा में स्थित है।"},
    {"question": "मधुबनी चित्रकला शैली किस राज्य से प्रसिद्ध है?", "options": ["बिहार", "पश्चिम बंगाल", "मध्य प्रदेश", "पंजाब"], "correct": 0, "explanation": "मधुबनी कला बिहार के मिथिला क्षेत्र से जुड़ी है।"},
    {"question": "कुचिपुड़ी किस राज्य का शास्त्रीय नृत्य है?", "options": ["केरल", "आंध्र प्रदेश", "ओडिशा", "मणिपुर"], "correct": 1, "explanation": "कुचिपुड़ी आंध्र प्रदेश का शास्त्रीय नृत्य है।"},
    {"question": "भरतनाट्यम किस राज्य का प्रसिद्ध नृत्य है?", "options": ["तमिलनाडु", "केरल", "कर्नाटक", "आंध्र प्रदेश"], "correct": 0, "explanation": "भरतनाट्यम तमिलनाडु का शास्त्रीय नृत्य है।"},
    {"question": "बिहू किस राज्य का लोकप्रिय नृत्य है?", "options": ["असम", "पंजाब", "बंगाल", "ओडिशा"], "correct": 0, "explanation": "बिहू असम का लोक नृत्य है।"},
    {"question": "हम्पी के खंडर किस राज्य में स्थित हैं?", "options": ["कर्नाटक", "महाराष्ट्र", "आंध्र प्रदेश", "तमिलनाडु"], "correct": 0, "explanation": "हम्पी के ऐतिहासिक खंडर कर्नाटक में स्थित हैं।"},
    {"question": "अजंता की गुफाएँ कहाँ स्थित हैं?", "options": ["महाराष्ट्र", "मध्य प्रदेश", "राजस्थान", "बिहार"], "correct": 0, "explanation": "अजंता और एलोरा की गुफाएं औरंगाबाद (महाराष्ट्र) में हैं।"},
    {"question": "राष्ट्रीय गीत 'वंदे मातरम' के रचयिता कौन हैं?", "options": ["बंकिमचंद्र चटर्जी", "रविंद्रनाथ टैगोर", "محمد اقبال", "शरद चंद्र"], "correct": 0, "explanation": "बंकिमचंद्र चटर्जी इसके रचनाकार हैं।"},
    {"question": "भारत का राष्ट्रीय गान 'जन गण मन' किसने लिखा है?", "options": ["रविंद्रनाथ टैगोर", "बंकिमचंद्र चटर्जी", "प्रेमचंद", "निराला"], "correct": 0, "explanation": "रविंद्रनाथ टैगोर ने जन गण मन लिखा है।"},
    {"question": "प्रसिद्ध खजुराहो के मंदिर किस राज्य में हैं?", "options": ["मध्य प्रदेश", "उत्तर प्रदेश", "राजस्थान", "गुजरात"], "correct": 0, "explanation": "खजुराहो के मंदिर मध्य प्रदेश के छतरपुर में हैं।"},
    {"question": "तंजौर का राजराजेश्वर मंदिर किसने बनवाया था?", "options": ["राजराज चोल प्रथम", "राजेंद्र चोल", "कृष्ण देव राय", "कनिष्क"], "correct": 0, "explanation": "इसे राजराज चोल प्रथम ने बनवाया था।"},
    {"question": "लावणी किस राज्य का लोकप्रिय नृत्य है?", "options": ["महाराष्ट्र", "गुजरात", "पंजाब", "राजस्थान"], "correct": 0, "explanation": "लावणी महाराष्ट्र का प्रसिद्ध लोक नृत्य है।"},
    {"question": "यक्षगान किस राज्य की नृत्य कला है?", "options": ["कर्नाटक", "केरल", "तमिलनाडु", "आंध्र प्रदेश"], "correct": 0, "explanation": "यक्षगान कर्नाटक की पारंपरिक नृत्य शैली है।"},
    {"question": "गरबा नृत्य किस राज्य से संबंधित है?", "options": ["गुजरात", "राजस्थान", "महाराष्ट्र", "पंजाब"], "correct": 0, "explanation": "गरबा गुजरात का बहुत लोकप्रिय नृत्य है।"},
    {"question": "भांगड़ा और गिद्दा कहाँ के प्रसिद्ध लोक नृत्य हैं?", "options": ["पंजाब", "हरियाणा", "राजस्थान", "उत्तर प्रदेश"], "correct": 0, "explanation": "भांगड़ा और गिद्दा पंजाब के लोक नृत्य हैं।"},
    {"question": "पंडित रविशंकर किस वाद्य यंत्र से जुड़े हैं?", "options": ["सतार", "तबल", "बांसुरी", "सरोद"], "correct": 0, "explanation": "पंडित रविशंकर विश्व प्रसिद्ध सितार वादक थे।"},
    {"question": "उस्ताद बिस्मिल्लाह खान क्या बजाते थे?", "options": ["शहनाई", "बांसुरी", "सितार", "संतूर"], "correct": 0, "explanation": "उस्ताद बिस्मिल्लाह खान भारत के महान शहनाई वादक थे।"},
    {"question": "हरिप्रसाद चौरसिया का संबंध किस वाद्य यंत्र से है?", "options": ["बांसुरी", "सितार", "तबल", "वीणा"], "correct": 0, "explanation": "हरिप्रसाद चौरसिया प्रसिद्ध बांसुरी वादक हैं।"},
    {"question": "सरोद वादक अमजद अली खान का संबंध किससे है?", "options": ["सरोद", "सितार", "संतूर", "गिटार"], "correct": 0, "explanation": "वे भारत के प्रतिष्ठित सरोद वादक हैं।"},
    {"question": "मास्टर आर्मेनिया चित्रकला शैली का संबंध किससे है?", "options": ["राजा रवि वर्मा", "नंदलाल बोस", "यामिनी राय", "एम. एफ. हुसैन"], "correct": 0, "explanation": "आधुनिक भारतीय चित्रकला में राजा रवि वर्मा बहुत प्रसिद्ध हैं।"},
    {"question": "मोहिनीअट्टम किस राज्य का शास्त्रीय नृत्य है?", "options": ["केरल", "तमिलनाडु", "कर्नाटक", "आंध्र प्रदेश"], "correct": 0, "explanation": "मोहिनीअट्टम केरल का शास्त्रीय नृत्य है।"},
    {"question": "ओडिसी नृत्य किस राज्य का शास्त्रीय नृत्य है?", "options": ["ओडिशा", "पश्चिम बंगाल", "बिहार", "झारखंड"], "correct": 0, "explanation": "ओडिसी ओडिशा का पारंपरिक शास्त्रीय नृत्य है।"},
    {"question": "मणिपुरी नृत्य का संबंध किस राज्य से है?", "options": ["मणिपुर", "त्रिपुरा", "असम", "मेघालय"], "correct": 0, "explanation": "मणिपुरी नृत्य मणिपुर राज्य का है।"},
    {"question": "सत्रिया नृत्य किस राज्य का शास्त्रीय नृत्य है?", "options": ["असम", "मणिपुर", "त्रिपुरा", "सिक्किम"], "correct": 0, "explanation": "सत्रिया असम का शास्त्रीय नृत्य है।"},
    {"question": "फतेहपुर सीकरी का निर्माण किसने करवाया था?", "options": ["अकबर", "शाहजहाँ", "हुमायूँ", "बाबर"], "correct": 0, "explanation": "मुगल सम्राट अकबर ने फतेहपुर सीकरी बनवाई थी।"},
    {"question": "जामा मस्जिद (दिल्ली) का निर्माण किसने करवाया?", "options": ["शाहजहाँ", "औरंगजेब", "अकबर", "جهانگیر"], "correct": 0, "explanation": "शाहजहाँ ने दिल्ली की जामा मस्जिद बनवाई थी।"},
    {"question": "लाल किले का निर्माण किसने करवाया था?", "options": ["शाहजहाँ", "अकबर", "शेरशाह सूरी", "कुतुबुद्दीन ऐबक"], "correct": 0, "explanation": "दिल्ली का लाल किला शाहजहाँ द्वारा बनवाया गया था।"},
    {"question": "चारमीनार का निर्माण किसने करवाया था?", "options": ["मुहम्मद कुली कुतुबशाह", "इब्राहिम आदिल शाह", "अकबर", "फिरोजशाह तुगलक"], "correct": 0, "explanation": "कुली कुतुबशाह ने 1591 में चारमीनार बनवाई थी।"},
    {"question": "इमामबाड़ा कहाँ स्थित है?", "options": ["लखनऊ", "आगरा", "दिल्ली", "हैदराबाद"], "correct": 0, "explanation": "बड़ा इमामबाड़ा लखनऊ (उत्तर प्रदेश) में स्थित है।"},
    {"question": "भारत भवन कहाँ स्थित है?", "options": ["भोपाल", "दिल्ली", "जयपुर", "मुंबई"], "correct": 0, "explanation": "भारत भवन भोपाल (मध्य प्रदेश) में एक कला केंद्र है।"},
    {"question": "सांची का स्तूप किस राज्य में स्थित है?", "options": ["मध्य प्रदेश", "उत्तर प्रदेश", "बिहार", "छत्तीसगढ़"], "correct": 0, "explanation": "सांची का महान बौद्ध स्तूप मध्य प्रदेश में है।"},
    {"question": "अमरनाथ गुफा किस राज्य या केंद्र शासित प्रदेश में है?", "options": ["जम्मू और कश्मीर", "उत्तराखंड", "हिमाचल प्रदेश", "लद्दाख"], "correct": 0, "explanation": "अमरनाथ पवित्र गुफा जम्मू और कश्मीर में स्थित है।"},
    {"question": "वैष्णो देवी मंदिर कहाँ स्थित है?", "options": ["कटरा (जम्मू)", "श्रीनगर", "शिमला", "हरिद्वार"], "correct": 0, "explanation": "माँ वैष्णो देवी का धाम कटरा, जम्मू में है।"},
    {"question": "दिलवाड़ा जैन मंदिर कहाँ स्थित है?", "options": ["माउंट आबू (राजस्थान)", "अमरनाथ", "पुरी", "वाराणसी"], "correct": 0, "explanation": "दिलवाड़ा के प्रसिद्ध जैन मंदिर माउंट आबू में हैं।"},
    {"question": "मीनाक्षी मंदिर कहाँ स्थित है?", "options": ["मदुरै", "तंजावर", "कांचीपुरम", "वेलोर"], "correct": 0, "explanation": "प्रसिद्ध मीनाक्षी अम्मन मंदिर मदुरै (तमिलनाडु) में है।"},
    {"question": "बद्रीनाथ धाम किस राज्य में स्थित है?", "options": ["उत्तराखंड", "हिमाचल प्रदेश", "जम्मू कश्मीर", "सिक्किम"], "correct": 0, "explanation": "बद्रीनाथ उत्तराखंड के चमोली जिले में है।"},
    {"question": "केदारनाथ मंदिर किस नदी के तट पर है?", "options": ["मंदाकिनी", "अलकनंदा", "भागीरथी", "यमुना"], "correct": 0, "explanation": "केदारनाथ मंदिर मंदाकिनी नदी के तट पर स्थित है।"},
    {"question": "जगन्नाथ पुरी मंदिर किस राज्य में है?", "options": ["ओडिशा", "पश्चिम बंगाल", "आंध्र प्रदेश", "तमिलनाडु"], "correct": 0, "explanation": "जगन्नाथ पुरी का मंदिर ओडिशा में है।"},
    {"question": "महाबोधि मंदिर कहाँ स्थित है?", "options": ["बोधगया (बिहार)", "सारनाथ", "कुशीनगर", "राजगीर"], "correct": 0, "explanation": "महाबोधि मंदिर बोधगया में स्थित है।"},
    {"question": "महाबलीपुरम के रथ मंदिरों का निर्माण किसने करवाया था?", "options": ["पल्लव राजाओं ने", "चोल राजाओं ने", "गुप्त राजाओं ने", "चालुक्य राजाओं ने"], "correct": 0, "explanation": "पल्लव राजवंश के राजाओं ने इन्हें बनवाया था।"},
    {"question": "एलीफेंटा की गुफाएँ कहाँ स्थित हैं?", "options": ["मुंबई के पास", "औरंगाबाद", "गोवा", "पुणे"], "correct": 0, "explanation": "एलीफेंटा गुफाएं मुंबई के पास अरब सागर में द्वीप पर हैं।"},
    {"question": "राष्ट्रीय फिल्म संग्रहालय कहाँ स्थित है?", "options": ["मुंबई", "पुणे", "नई दिल्ली", "कोलकाता"], "correct": 0, "explanation": "राष्ट्रीय फिल्म संग्रहालय पुणे, महाराष्ट्र में है।"},
    {"question": "संगीत नाटक अकादमी की स्थापना कब हुई थी?", "options": ["1953", "1950", "1956", "1960"], "correct": 0, "explanation": "संगीत नाटक अकादमी की स्थापना 1953 में हुई थी।"},
    {"question": "ललित कला अकादमी की स्थापना कब हुई?", "options": ["1954", "1952", "1958", "1962"], "correct": 0, "explanation": "ललित कला अकादमी की स्थापना 1954 में हुई थी।"},
    {"question": "साहित्य अकादमी की स्थापना कब हुई थी?", "options": ["1954", "1950", "1960", "1947"], "correct": 0, "explanation": "साहित्य अकादमी की स्थापना 1954 में हुई थी।"},
    {"question": "भारतीय शास्त्रीय संगीत का मुख्य ग्रंथ किसे माना जाता है?", "options": ["नाट्यशास्त्र", "संगीत रत्नाकर", "ऋग्वेद", "सामवेद"], "correct": 0, "explanation": "भरत मुनि रचित 'नाट्यशास्त्र' को मुख्य ग्रंथ माना जाता है।"},
    {"question": "बिहू महोत्सव मुख्य रूप से किस राज्य में मनाया जाता है?", "options": ["असम", "मेघालय", "त्रिपुरा", "मणिपुर"], "correct": 0, "explanation": "असम में बिहू वर्ष में तीन बार मनाया जाता है।"},
    {"question": "छऊ नृत्य किस राज्य से संबंधित है?", "options": ["झारखंड, पश्चिम बंगाल, ओडिशा", "पंजाब और हरियाणा", "बिहार और यूपी", "केरल और तमिलनाडु"], "correct": 0, "explanation": "छऊ एक प्रसिद्ध अर्ध-शास्त्रीय नृत्य है जो पूर्वी भारत में प्रचलित है।"}
]

# चैट गेम ट्रैकर
active_games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 **नमस्ते! आपका स्वागत है BrainX Quiz Pro Bot में।**\n\n"
        "🎮 धमाकेदार क्विज़ खेलने के लिए नीचे दी गई कमांड्स भेजें:\n"
        "👉 **`/gkquiz`** - 50 महत्वपूर्ण GK PYQ Quiz\n"
        "👉 **`/hindiquiz`** - 30 हिंदी व्याकरण Quiz\n"
        "👉 **`/englishquiz`** - 20 English Grammar Quiz\n"
        "👉 **`/artquiz`** - 50 कला एवं संस्कृति (Art & Culture) Quiz\n\n"
        "⏱️ *हर सवाल के लिए 15 सेकंड का समय मिलेगा, जिसके बाद अगला सवाल स्वतः आ जाएगा!*"
    )

async def start_quiz_session(update: Update, context: ContextTypes.DEFAULT_TYPE, q_list, quiz_name):
    chat_id = update.effective_chat.id
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await update.message.reply_text("⚠️ इस चैट में पहले से क्विज़ चल रहा है! कृपया उसे पूरा होने दें।")
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
        "🎯 कुल प्रश्न: " + str(len(q_list)) + " | प्रति प्रश्न समय: 15 सेकंड। तैयार हो जाइए!"
    )
    await asyncio.sleep(1.5)
    await send_next_question(chat_id, context)

async def gk_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, GK_QUESTIONS, "GK PYQ (50 प्रश्न)")

async def hindi_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, HINDI_QUESTIONS, "Hindi (30 प्रश्न)")

async def english_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, ENGLISH_QUESTIONS, "English (20 प्रश्न)")

async def art_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_quiz_session(update, context, ART_QUESTIONS, "Art & Culture (50 प्रश्न)")

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
    
    # Telegram Poll Format (15 सेकंड टाइमर के साथ)
    await context.bot.send_poll(
        chat_id=chat_id,
        question=f"[{game['quiz_name']}] प्रश्न {q_idx + 1} / {len(q_list)}:\n{q_data['question']}",
        options=q_data["options"],
        type="quiz",
        correct_option_id=q_data["correct"],
        is_anonymous=False,
        explanation=q_data["explanation"],
        open_period=15  # ⏱️ 15 सेकंड पोल टाइमर
    )
    
    game["current_q"] += 1
    
    # 16 सेकंड बाद अगला सवाल ऑटोमैटिक भेजा जाएगा
    await asyncio.sleep(16)
    
    if chat_id in active_games and active_games[chat_id]["active"]:
        await send_next_question(chat_id, context)

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
    q_list = game["questions"]
    
    if q_idx < 0 or q_idx >= len(q_list):
        return

    correct_opt = q_list[q_idx]["correct"]
    
    if user_id not in game["scores"]:
        game["scores"][user_id] = {"name": user_name, "score": 0}

    if correct_opt in selected_options:
        game["scores"][user_id]["score"] += 1

async def show_final_leaderboard(chat_id, context):
    game = active_games[chat_id]
    game["active"] = False
    scores_dict = game["scores"]
    quiz_name = game["quiz_name"]

    if not scores_dict:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🏁 **{quiz_name} समाप्त!** किसी ने उत्तर नहीं दिया। अगली बार फिर प्रयास करें! 💪"
        )
        return

    sorted_players = sorted(scores_dict.values(), key=lambda x: x["score"], reverse=True)
    first_winner = sorted_players[0]
    second_winner = sorted_players[1] if len(sorted_players) > 1 else None
    third_winner = sorted_players[2] if len(sorted_players) > 2 else None

    report = f"🏆 **====================** 🏆\n"
    report += f"   🌟 **{quiz_name.upper()} LEADERBOARD** 🌟\n"
    report += f"🏆 **====================** 🏆\n\n"

    report += f"👑 **CHAMPION OF THE MATCH** 👑\n"
    report += f"🎉 दिल से बहुत-बहुत बधाई **{first_winner['name']}** जी! 🥇\n"
    report += f"🔥 आपने शानदार प्रदर्शन करते हुए सबसे ज्यादा **{first_winner['score']}** अंक हासिल किए हैं और बाजी मार ली! आप वाकई जीनियस हैं! 🚀\n\n"

    if second_winner:
        report += f"🥈 **दूसरा स्थान:** {second_winner['name']} (स्कोर: {second_winner['score']})\n"
    if third_winner:
        report += f"🥉 **तीसरा स्थान:** {third_winner['name']} (स्कोर: {third_winner['score']})\n"

    report += "\n📜 **सभी खिलाड़ियों की पूरी सूची (Scoreboard):**\n"
    report += "----------------------------------------\n"

    for idx, player in enumerate(sorted_players, start=1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
        report += f"{medal} **{player['name']}** — {player['score']} Points\n"

    report += "----------------------------------------\n"
    report += "💖 *हार-जीत तो खेल का हिस्सा है, असली मकसद सीखना है। आप सभी हमारे विजेता हैं!* ✨"

    await context.bot.send_message(chat_id=chat_id, text=report)

async def main():
    TOKEN = "8959348945:AAFTYLkJ-q40V46PR-InXwIG0qU3kpDLXig"
    
    await start_web_server()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gkquiz", gk_cmd))
    app.add_handler(CommandHandler("hindiquiz", hindi_cmd))
    app.add_handler(CommandHandler("englishquiz", english_cmd))
    app.add_handler(CommandHandler("artquiz", art_cmd))
    app.add_handler(PollAnswerHandler(receive_poll_answer))

    print("BrainX Full Quiz Bot live with 15s timer...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
