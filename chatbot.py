"""LeafScan AI v4 — Agriculture Chatbot with Multilingual Support"""

LANGUAGES = {
    'en': {'name': 'English',     'flag': '🇬🇧', 'native': 'English'},
    'hi': {'name': 'Hindi',       'flag': '🇮🇳', 'native': 'हिन्दी'},
    'bn': {'name': 'Bengali',     'flag': '🇧🇩', 'native': 'বাংলা'},
    'te': {'name': 'Telugu',      'flag': '🇮🇳', 'native': 'తెలుగు'},
    'mr': {'name': 'Marathi',     'flag': '🇮🇳', 'native': 'मराठी'},
    'ta': {'name': 'Tamil',       'flag': '🇮🇳', 'native': 'தமிழ்'},
    'gu': {'name': 'Gujarati',    'flag': '🇮🇳', 'native': 'ગુજરાતી'},
    'pa': {'name': 'Punjabi',     'flag': '🇮🇳', 'native': 'ਪੰਜਾਬੀ'},
    'ur': {'name': 'Urdu',        'flag': '🇵🇰', 'native': 'اردو'},
    'kn': {'name': 'Kannada',     'flag': '🇮🇳', 'native': 'ಕನ್ನಡ'},
    'ml': {'name': 'Malayalam',   'flag': '🇮🇳', 'native': 'മലയാളം'},
    'or': {'name': 'Odia',        'flag': '🇮🇳', 'native': 'ଓଡ଼ିଆ'},
    'zh': {'name': 'Chinese',     'flag': '🇨🇳', 'native': '中文'},
    'es': {'name': 'Spanish',     'flag': '🇪🇸', 'native': 'Español'},
    'fr': {'name': 'French',      'flag': '🇫🇷', 'native': 'Français'},
    'ar': {'name': 'Arabic',      'flag': '🇸🇦', 'native': 'العربية'},
    'sw': {'name': 'Swahili',     'flag': '🇰🇪', 'native': 'Kiswahili'},
    'pt': {'name': 'Portuguese',  'flag': '🇧🇷', 'native': 'Português'},
}

# Greeting translations
GREETINGS = {
    'en': "Hello! I'm KrishiBot 🌿, your AI agriculture assistant. I can help you with plant diseases, crop care, pest control, soil health, and farming best practices. What's your question?",
    'hi': "नमस्ते! मैं KrishiBot 🌿 हूं, आपका AI कृषि सहायक। मैं पौधों की बीमारियों, फसल देखभाल, कीट नियंत्रण, मिट्टी स्वास्थ्य और खेती में आपकी मदद कर सकता हूं। आपका प्रश्न क्या है?",
    'bn': "নমস্কার! আমি KrishiBot 🌿, আপনার AI কৃষি সহায়ক। আমি উদ্ভিদ রোগ, ফসল যত্ন, কীটপতঙ্গ নিয়ন্ত্রণ, মাটির স্বাস্থ্য এবং কৃষিতে সাহায্য করতে পারি।",
    'te': "నమస్కారం! నేను KrishiBot 🌿, మీ AI వ్యవసాయ సహాయకుడు. నేను మొక్క వ్యాధులు, పంట సంరక్షణ, తెగుళ్ళ నియంత్రణలో సహాయం చేయగలను.",
    'mr': "नमस्कार! मी KrishiBot 🌿, तुमचा AI कृषी सहाय्यक. मी वनस्पती रोग, पीक काळजी, कीड नियंत्रण यामध्ये मदत करू शकतो.",
    'ta': "வணக்கம்! நான் KrishiBot 🌿, உங்கள் AI விவசாய உதவியாளர். தாவர நோய்கள், பயிர் பராமரிப்பு, பூச்சி கட்டுப்பாடு பற்றி உதவுவேன்.",
    'gu': "નમસ્તે! હું KrishiBot 🌿, તમારો AI કૃષિ સહાયક. હું છોડ રોગ, પાક સંભાળ, જંતુ નિયંત્રણ, માટી સ્વાસ્થ્ય વિશે મદદ કરી શકું.",
    'pa': "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ KrishiBot 🌿 ਹਾਂ, ਤੁਹਾਡਾ AI ਖੇਤੀਬਾੜੀ ਸਹਾਇਕ। ਮੈਂ ਪੌਦਿਆਂ ਦੀਆਂ ਬਿਮਾਰੀਆਂ, ਫ਼ਸਲਾਂ ਦੀ ਦੇਖਭਾਲ ਵਿੱਚ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ।",
    'es': "¡Hola! Soy KrishiBot 🌿, tu asistente agrícola de IA. Puedo ayudarte con enfermedades de plantas, cuidado de cultivos y control de plagas.",
    'fr': "Bonjour! Je suis KrishiBot 🌿, votre assistant agricole IA. Je peux vous aider avec les maladies des plantes, les soins des cultures et la lutte antiparasitaire.",
    'zh': "你好！我是KrishiBot 🌿，您的AI农业助手。我可以帮助您了解植物病害、作物护理、害虫防治和土壤健康。",
    'ar': "مرحبًا! أنا KrishiBot 🌿، مساعدك الزراعي بالذكاء الاصطناعي. يمكنني مساعدتك في أمراض النباتات ورعاية المحاصيل ومكافحة الآفات.",
    'sw': "Habari! Mimi ni KrishiBot 🌿, msaidizi wako wa kilimo wa AI. Ninaweza kukusaidia na magonjwa ya mimea, utunzaji wa mazao na udhibiti wa wadudu.",
    'pt': "Olá! Sou o KrishiBot 🌿, seu assistente agrícola de IA. Posso ajudá-lo com doenças de plantas, cuidados com culturas e controle de pragas.",
}

# Agriculture knowledge base (keyword → response per language)
AGRI_KB = {
    # ── Watering ────────────────────────────────────────────
    'water|irrigation|watering|पानी|सिंचाई|জল|পানি': {
        'en': "💧 **Watering Best Practices:**\n• Water deeply but less often (2–3x/week) rather than shallow daily\n• Always water at the **base** of plants, never on leaves\n• Morning watering is ideal — leaves dry before evening, reducing fungal risk\n• Use **drip irrigation** to save 40% water and reduce disease\n• Check soil moisture 5cm deep before watering — if moist, skip it\n• Avoid waterlogging — it causes root rot in most crops",
        'hi': "💧 **पानी देने की सर्वोत्तम विधियां:**\n• रोज़ थोड़ा पानी देने के बजाय गहरा लेकिन कम बार (हफ्ते में 2-3 बार) पानी दें\n• हमेशा पौधे की **जड़ में** पानी दें, पत्तियों पर नहीं\n• सुबह पानी देना सबसे अच्छा है - पत्तियां शाम से पहले सूख जाती हैं\n• **ड्रिप सिंचाई** का उपयोग करें - 40% पानी बचाएं और रोग कम करें\n• पानी देने से पहले 5 सेमी गहरी मिट्टी की नमी जांचें",
        'bn': "💧 **জল দেওয়ার সেরা পদ্ধতি:**\n• প্রতিদিন অল্প জল না দিয়ে গভীরভাবে কিন্তু কম ঘন ঘন (সপ্তাহে 2-3 বার) জল দিন\n• সবসময় গাছের **গোড়ায়** জল দিন, পাতায় নয়\n• সকালে জল দেওয়া আদর্শ — পাতা সন্ধ্যার আগে শুকিয়ে যায়",
    },
    # ── Fertilizer ──────────────────────────────────────────
    'fertilizer|npk|compost|manure|खाद|उर्वरक|সার|সারের': {
        'en': "🌱 **Fertilization Guide:**\n• **NPK basics:** N (Nitrogen) = leaf growth | P (Phosphorus) = roots & flowers | K (Potassium) = fruit & disease resistance\n• Apply nitrogen in **vegetative stage**, reduce at flowering\n• Organic compost improves soil structure AND provides slow-release nutrients\n• **Don't over-fertilize** — excess nitrogen makes plants succulent and more disease-prone\n• Side-dress with compost every 4–6 weeks for continuous feeding\n• Foliar sprays work fast for deficiency correction",
        'hi': "🌱 **उर्वरक मार्गदर्शिका:**\n• **NPK मूल बातें:** N (नाइट्रोजन) = पत्ती वृद्धि | P (फास्फोरस) = जड़ें और फूल | K (पोटेशियम) = फल और रोग प्रतिरोध\n• **वानस्पतिक अवस्था** में नाइट्रोजन डालें, फूल आने पर कम करें\n• जैविक खाद मिट्टी की संरचना सुधारती है और धीरे-धीरे पोषण देती है\n• **अधिक उर्वरक न डालें** — अतिरिक्त नाइट्रोजन पौधों को रोग के प्रति अधिक संवेदनशील बनाती है",
        'bn': "🌱 **সার প্রয়োগ নির্দেশিকা:**\n• NPK মূল বিষয়: N (নাইট্রোজেন) = পাতার বৃদ্ধি | P (ফসফরাস) = শিকড় ও ফুল | K (পটাসিয়াম) = ফল ও রোগ প্রতিরোধ\n• জৈব কম্পোস্ট মাটির গঠন উন্নত করে এবং ধীরে ধীরে পুষ্টি সরবরাহ করে",
    },
    # ── Pest control ─────────────────────────────────────────
    'pest|insect|bug|aphid|whitefly|कीट|कीड़ा|পোকা|পোকামাকড়': {
        'en': "🐛 **Pest Control Strategies:**\n• **First line:** Inspect plants weekly — catch pests early before populations explode\n• **Physical:** Yellow sticky traps (free monitoring), hand-picking large pests\n• **Organic options:** Neem oil spray (2tbsp/L), insecticidal soap, diatomaceous earth\n• **Biological control:** Release ladybugs for aphids, Trichogramma wasps for caterpillars\n• **Chemical (last resort):** Use targeted insecticides, avoid broad-spectrum that kills beneficial insects\n• Always spray in **early morning or evening** — midday spraying burns leaves and harms bees",
        'hi': "🐛 **कीट नियंत्रण रणनीतियां:**\n• **पहला कदम:** साप्ताहिक पौधों का निरीक्षण करें — जल्दी पकड़ें\n• **भौतिक:** पीले चिपचिपे जाल, बड़े कीटों को हाथ से चुनें\n• **जैविक विकल्प:** नीम तेल स्प्रे (2 बड़े चम्मच/लीटर), कीटनाशक साबुन\n• **जैव नियंत्रण:** एफिड्स के लिए लेडीबग छोड़ें\n• **रासायनिक (अंतिम उपाय):** लक्षित कीटनाशकों का उपयोग करें",
        'bn': "🐛 **কীট নিয়ন্ত্রণ কৌশল:**\n• সাপ্তাহিক পরিদর্শন করুন — আগে ধরুন\n• হলুদ আঠালো ফাঁদ, হাত দিয়ে বড় কীট তুলুন\n• জৈব বিকল্প: নিম তেল স্প্রে, কীটনাশক সাবান",
    },
    # ── Fungal disease ───────────────────────────────────────
    'fungal|fungus|mold|blight|rust|ফাংগাল|ছত্রাক|फंगल|कवक': {
        'en': "🍄 **Fighting Fungal Diseases:**\n• **Prevention is 90% of the battle** — good airflow, dry leaves, crop rotation\n• Space plants properly — crowded plants = humid microclimate = fungal paradise\n• Water at soil level, never overhead\n• **Copper-based fungicides** are broad-spectrum and organic-approved\n• **Neem oil** has antifungal properties (apply every 7–10 days preventively)\n• Remove infected leaves/plants immediately — don't compost them\n• **Baking soda spray** (1tbsp/L) changes leaf pH and inhibits many fungi",
        'hi': "🍄 **फफूंद रोगों से लड़ना:**\n• **रोकथाम 90% लड़ाई है** — अच्छा वायु प्रवाह, सूखी पत्तियां, फसल चक्र\n• पौधों को उचित दूरी पर लगाएं — भीड़भाड़ वाले पौधे = आर्द्र माइक्रोक्लाइमेट = कवक के लिए आदर्श\n• **कॉपर-आधारित फफूंदनाशक** व्यापक-स्पेक्ट्रम हैं और जैविक अनुमोदित हैं\n• संक्रमित पत्तियां/पौधे तुरंत हटाएं — उन्हें खाद में न डालें",
        'bn': "🍄 **ছত্রাকজনিত রোগ মোকাবেলা:**\n• প্রতিরোধই 90% যুদ্ধ — ভালো বায়ু চলাচল, শুষ্ক পাতা, ফসল পরিবর্তন\n• তামা-ভিত্তিক ছত্রাকনাশক ব্যবহার করুন\n• সংক্রামিত পাতা অবিলম্বে সরান — কম্পোস্টে দেবেন না",
    },
    # ── Soil health ──────────────────────────────────────────
    'soil|ph|compost|organic|मिट्टी|भूमि|মাটি|মৃত্তিকা': {
        'en': "🌍 **Soil Health Fundamentals:**\n• **Test soil pH** annually — most crops prefer 6.0–7.0\n• Add lime to raise pH (acidic soil), sulfur to lower pH (alkaline soil)\n• **Organic matter is king** — add compost every season to improve water retention, aeration, and microbial life\n• Avoid tilling wet soil — it destroys soil structure\n• **Cover crops** (legumes, clover) fix nitrogen and prevent erosion in off-season\n• Earthworms = healthy soil indicator — protect them by avoiding chemical overuse\n• Mulching retains moisture, regulates temperature, suppresses weeds",
        'hi': "🌍 **मिट्टी स्वास्थ्य की मूल बातें:**\n• सालाना **मिट्टी pH परीक्षण** करें — अधिकतर फसलें 6.0–7.0 पसंद करती हैं\n• अम्लीय मिट्टी के लिए चूना, क्षारीय मिट्टी के लिए सल्फर डालें\n• **जैविक पदार्थ राजा है** — हर मौसम में खाद डालें\n• गीली मिट्टी की जुताई से बचें — यह मिट्टी की संरचना नष्ट करती है",
        'bn': "🌍 **মাটির স্বাস্থ্যের মূল বিষয়:**\n• বার্ষিক মাটির pH পরীক্ষা করুন — বেশিরভাগ ফসল 6.0–7.0 পছন্দ করে\n• জৈব পদার্থ মাটির জলধারণ ক্ষমতা এবং বায়ুচলাচল উন্নত করে",
    },
    # ── Crop rotation ────────────────────────────────────────
    'rotation|rotate|crop rotation|फसल चक्र|ফসল পরিবর্তন': {
        'en': "🔄 **Crop Rotation Benefits & Guide:**\n• Breaks pest and disease cycles that build up in soil\n• Different crops extract and replenish different nutrients\n• **Simple 4-year rotation:** Leafy greens → Legumes → Root vegetables → Fruiting crops\n• **Never plant:** Same family crops in same spot 2 years in a row (e.g., tomato, potato, pepper = Solanaceae)\n• Legumes (beans, peas, clover) **fix nitrogen** — always follow with heavy feeders\n• Keep records of what you plant where each year",
        'hi': "🔄 **फसल चक्र के लाभ:**\n• मिट्टी में जमा होने वाले कीट और रोग चक्र को तोड़ता है\n• विभिन्न फसलें विभिन्न पोषक तत्वों को निकालती और भरती हैं\n• **सरल 4-साल का चक्र:** पत्तेदार सब्जियां → फलियां → जड़ सब्जियां → फल देने वाली फसलें",
        'bn': "🔄 **ফসল পরিবর্তনের সুবিধা:**\n• মাটিতে জমা কীট ও রোগ চক্র ভাঙে\n• সহজ 4 বছরের রোটেশন: পাতাসবজি → ফলিয়া → মূলসবজি → ফলের ফসল",
    },
    # ── Tomato care ──────────────────────────────────────────
    'tomato|টমেটো|टमाटर': {
        'en': "🍅 **Tomato Growing Mastery:**\n• **Transplant deep** — bury stem up to first true leaves, develops strong root system\n• Stake/cage all plants — improves airflow and reduces disease by 40%\n• **Prune suckers** in indeterminate varieties for better fruit size\n• Consistent watering prevents **blossom end rot** (calcium deficiency from irregular watering)\n• **Common diseases:** Early blight, Late blight, Septoria leaf spot, Bacterial spot\n• Fertilize with balanced NPK early, switch to low-N high-K/P at flowering\n• Harvest when fully colored for best flavor",
        'hi': "🍅 **टमाटर उगाने की महारत:**\n• **गहरा रोपें** — पहली असली पत्तियों तक तना दबाएं, मजबूत जड़ प्रणाली विकसित होती है\n• सभी पौधों को दांव/पिंजरे दें — वायु प्रवाह में सुधार और 40% रोग कम करें\n• **आम रोग:** प्रारंभिक झुलसा, देर से झुलसा, सेप्टोरिया, बैक्टीरियल स्पॉट",
        'bn': "🍅 **টমেটো চাষের দক্ষতা:**\n• গভীরভাবে রোপণ করুন — প্রথম পাতা পর্যন্ত কাণ্ড পুঁতুন\n• সব গাছ খুঁটি দিন — বায়ুচলাচল উন্নত করে এবং 40% রোগ কমায়",
    },
    # ── Organic farming ──────────────────────────────────────
    'organic|जैविक|জৈব|natural farming|प्राकृतिक खेती': {
        'en': "🌿 **Organic Farming Essentials:**\n• **Soil first** — healthy soil = healthy plants = fewer pests and diseases\n• **Compost tea** — brew compost in water 24-48hrs, apply as foliar spray for microbial boost\n• **Neem** is the organic farmer's best friend — repels insects, fights fungi, systemic action\n• **Companion planting:** Basil near tomatoes (repels aphids), marigolds around borders (nematode control)\n• **Mulch everything** — suppresses weeds, retains moisture, adds organic matter as it breaks down\n• Certified organic: avoid all synthetic pesticides, herbicides, and chemical fertilizers",
        'hi': "🌿 **जैविक खेती की आवश्यक बातें:**\n• **पहले मिट्टी** — स्वस्थ मिट्टी = स्वस्थ पौधे = कम कीट और रोग\n• **नीम** जैविक किसान का सबसे अच्छा दोस्त है — कीड़ों को भगाता है, फफूंद से लड़ता है\n• **सहचर रोपण:** टमाटर के पास तुलसी (एफिड्स भगाती है), सीमाओं पर गेंदा",
        'bn': "🌿 **জৈব চাষের মূল বিষয়:**\n• প্রথমে মাটি — সুস্থ মাটি = সুস্থ গাছ = কম কীট ও রোগ\n• নিম জৈব কৃষকের সেরা বন্ধু — পোকা তাড়ায়, ছত্রাকের বিরুদ্ধে লড়ে",
    },
    # ── General help ─────────────────────────────────────────
    'help|कैसे|कैसे करें|সাহায্য|হেল্প|how|what|why': {
        'en': "🤝 **How I can help you:**\n• 🌿 **Plant diseases** — symptoms, treatment, prevention for 38+ diseases\n• 💊 **Treatment advice** — organic and chemical options\n• 🌱 **Crop care** — watering, fertilizing, pruning guides\n• 🐛 **Pest identification** — what's eating your crops and how to stop it\n• 🌍 **Soil health** — pH, composting, soil improvement\n• 🔄 **Crop rotation** — planning your seasonal rotation\n• 📅 **Seasonal tips** — what to do each month\n\nJust ask me anything about your crops! 🌾",
        'hi': "🤝 **मैं कैसे मदद कर सकता हूं:**\n• 🌿 **पौधों की बीमारियां** — 38+ बीमारियों के लक्षण, उपचार, रोकथाम\n• 💊 **उपचार सलाह** — जैविक और रासायनिक विकल्प\n• 🌱 **फसल देखभाल** — सिंचाई, उर्वरक, छंटाई गाइड\n• 🐛 **कीट पहचान** — क्या आपकी फसल खा रहा है और कैसे रोकें\n\nअपनी फसलों के बारे में कुछ भी पूछें! 🌾",
        'bn': "🤝 **আমি কীভাবে সাহায্য করতে পারি:**\n• 🌿 **উদ্ভিদ রোগ** — 38+ রোগের লক্ষণ, চিকিৎসা, প্রতিরোধ\n• 🌱 **ফসল যত্ন** — সেচ, সার, ছাঁটাই নির্দেশিকা\n• 🐛 **কীট সনাক্তকরণ** — কী আপনার ফসল খাচ্ছে এবং কীভাবে থামাবেন",
    },
}

def get_greeting(lang='en'):
    return GREETINGS.get(lang, GREETINGS['en'])

def get_bot_response(user_message, lang='en', context=None):
    """Generate agriculture chatbot response."""
    msg_lower = user_message.lower().strip()

    # Check knowledge base
    for keywords, responses in AGRI_KB.items():
        for kw in keywords.split('|'):
            if kw in msg_lower:
                resp = responses.get(lang) or responses.get('en', '')
                if resp:
                    return resp

    # Disease-specific responses
    diseases = {
        'late blight|late_blight|phytophthora': {
            'en': "⚠️ **Late Blight Emergency Response:**\nLate blight (Phytophthora infestans) is CRITICAL — can destroy your entire crop in 7–10 days!\n\n**Immediate steps:**\n1. Apply metalaxyl+mancozeb fungicide TODAY\n2. Remove ALL infected leaves/plants in sealed bags\n3. Do NOT compost infected material\n4. Warn neighboring farmers immediately\n5. Spray every 5 days — do not skip\n\n**Prevention:** Plant resistant varieties, avoid overhead watering, monitor weather forecasts.",
            'hi': "⚠️ **लेट ब्लाइट आपातकालीन प्रतिक्रिया:**\nलेट ब्लाइट (Phytophthora infestans) गंभीर है — 7–10 दिनों में पूरी फसल नष्ट कर सकती है!\n\n**तुरंत करें:**\n1. आज ही metalaxyl+mancozeb फफूंदनाशक लगाएं\n2. सभी संक्रमित पत्तियां/पौधे सील बैग में हटाएं\n3. संक्रमित सामग्री को खाद में न डालें\n4. पड़ोसी किसानों को तुरंत सूचित करें",
        },
        'early blight|alternaria': {
            'en': "🍅 **Early Blight Management:**\nEarly blight (Alternaria solani) is manageable with prompt action.\n\n**Treatment:**\n• Apply chlorothalonil or mancozeb fungicide\n• Remove infected lower leaves\n• Mulch soil to prevent spore splash\n• Spray every 7–10 days\n\n**Prevention:** Crop rotation (3 years), certified seeds, proper plant spacing.",
            'hi': "🍅 **प्रारंभिक झुलसा प्रबंधन:**\nप्रारंभिक झुलसा (Alternaria solani) को समय पर कार्रवाई से नियंत्रित किया जा सकता है।\n\n**उपचार:**\n• chlorothalonil या mancozeb फफूंदनाशक लगाएं\n• संक्रमित निचली पत्तियां हटाएं\n• मिट्टी के छींटे रोकने के लिए मल्च करें",
        },
    }

    for keywords, responses in diseases.items():
        for kw in keywords.split('|'):
            if kw in msg_lower:
                resp = responses.get(lang) or responses.get('en', '')
                if resp:
                    return resp

    # Seasonal advice
    if any(w in msg_lower for w in ['season|monsoon|summer|winter|kharif|rabi|खरीफ|रबी|বর্ষা'.split('|')]):
        return {
            'en': "📅 **Seasonal Farming Calendar:**\n\n🌸 **Spring (Feb–May):** Start seedlings indoors, prepare soil, apply preventive fungicides at first rains\n☀️ **Summer (May–Aug):** Kharif crops (rice, cotton, maize), increased pest pressure, monitor for spider mites in dry heat\n🍂 **Monsoon/Autumn (Aug–Oct):** High disease risk — fungal diseases explode in humidity. Apply copper fungicides preventively\n❄️ **Winter/Rabi (Oct–Feb):** Wheat, mustard, potato. Late blight risk for potatoes. Good time for soil improvement.",
            'hi': "📅 **मौसमी खेती कैलेंडर:**\n\n🌸 **वसंत (फरवरी–मई):** बीज घर के अंदर शुरू करें, मिट्टी तैयार करें\n☀️ **गर्मी (मई–अगस्त):** खरीफ फसलें — चावल, कपास, मक्का\n🍂 **मानसून/पतझड़ (अगस्त–अक्टूबर):** उच्च रोग जोखिम — तांबा फफूंदनाशक लगाएं\n❄️ **सर्दी/रबी (अक्टूबर–फरवरी):** गेहूं, सरसों, आलू",
        }.get(lang, {}).get('en') or "📅 I can advise on seasonal planting — tell me your location/crop for specific advice!"

    # Fallback responses by language
    fallbacks = {
        'en': f"🌿 I understand you're asking about: **'{user_message}'**\n\nI'm specialized in agriculture! Try asking me about:\n• Specific crop diseases (tomato blight, apple scab…)\n• Pest control methods\n• Watering and fertilization\n• Soil health\n• Organic farming\n• Crop rotation\n\nFor disease diagnosis, use the **🔬 Scan** feature to upload a leaf photo!",
        'hi': f"🌿 मैं समझता हूं आप '**{user_message}**' के बारे में पूछ रहे हैं।\n\nमैं कृषि में विशेषज्ञ हूं! पूछें:\n• विशिष्ट फसल रोग\n• कीट नियंत्रण\n• सिंचाई और उर्वरक\n• मिट्टी स्वास्थ्य\n\nरोग निदान के लिए **🔬 स्कैन** सुविधा का उपयोग करें!",
        'bn': f"🌿 আমি বুঝতে পারছি আপনি '**{user_message}**' সম্পর্কে জিজ্ঞেস করছেন।\n\nআমি কৃষিতে বিশেষজ্ঞ! জিজ্ঞেস করুন:\n• নির্দিষ্ট ফসলের রোগ\n• কীট নিয়ন্ত্রণ\n• সেচ ও সার\n• মাটির স্বাস্থ্য",
    }
    return fallbacks.get(lang, fallbacks['en'])