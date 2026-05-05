# لیست کلمات کلیدی برای فیلتر اخبار مرتبط با ایران
IRAN_KEYWORDS = [
    "ایران", "تهران", "آیت‌الله", "خامنه‌ای", "برجام", "تحریم", 
    "انرژی اتمی", "نیروگاه", "بازار تهران", "ریال", "تومان",
    "Iran", "Tehran", "Nuclear", "Sanctions", "Oil"
]

# کلمات کلیدی برای دسته‌بندی اخبار (تگ‌ها)
TAG_KEYWORDS = {
    "سیاسی": ["سیاست", "دیپلماسی", "نفتوگاز", "پارلمان", "رئیس‌جمهور", "Politics", "Diplomacy"],
    "اقتصادی": ["اقتصاد", "بورس", "بانک", "تورم", "نفت", "پول", "Economy", "Stock", "Inflation"],
    "نظامی": ["ارتش", "پدافند", "موشک", "جنگ", "نظامی", "Military", "Weapon", "Defense"],
    "اجتماعی": ["فرهنگ", "سلامت", "آموزش", "محیط زیست", "Social", "Health", "Education"]
}

# کلمات کلیدی برای محاسبه فوریت (Urgency)
URGENCY_KEYWORDS = {
    "high": ["فوری", "بحران", "حمله", "جنگ", "انفجار", "Emergency", "Crisis", "Attack", "War"],
    "medium": ["توافق", "دیدار", "اعلام", "گزارش", "Meeting", "Agreement", "Report"]
}

# کلمات کلیدی برای محاسبه احساس (Sentiment)
SENTIMENT_KEYWORDS = {
    "positive": ["موفقیت", "رشد", "توافق", "آرامش", "پیروزی", "Success", "Growth", "Peace", "Victory"],
    "negative": ["شکست", "تحریم", "جنگ", "فاجعه", "بحران", "Collapse", "Sanction", "War", "Disaster"]
}

# منابع RSS
RSS_FEEDS = {
    "BBC_Farsi": {
        "url": "http://feeds.bbci.co.uk/persian/rss.xml"
    },
    "Radio_Javan": {
        "url": "https://radiojavan.com/rss/news" # مثال
    },
    "Al Jazeera": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml"
    }
}
