"""
تنظیمات ربات خبرخوان
"""

RSS_FEEDS = {
    "Reuters": {"url": "https://feeds.reuters.com/reuters/topNews", "category": "general"},
    "CNN": {"url": "http://rss.cnn.com/rss/edition.rss", "category": "general"},
    "BBC": {"url": "http://feeds.bbci.co.uk/news/world/rss.xml", "category": "general"},
    "Washington Post": {"url": "https://feeds.washingtonpost.com/rss/world", "category": "general"},
    "Al Jazeera": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "category": "general"},
    "France24": {"url": "https://www.france24.com/fr/rss", "category": "general"},
    "AP News": {"url": "https://rsshub.app/apnews/topics/apf-topnews", "category": "general"},
    "The Guardian": {"url": "https://www.theguardian.com/world/rss", "category": "general"},
    "Sky News": {"url": "https://feeds.skynews.com/feeds/rss/world-news.xml", "category": "general"},
    "NBC News": {"url": "https://www.nbcnews.com/feeds/rss/topstories", "category": "general"},
    "CBS News": {"url": "https://www.cbsnews.com/rss/main/", "category": "general"},
    "NPR": {"url": "https://feeds.npr.org/1001/rss.xml", "category": "general"},
    "Euronews": {"url": "https://feeds.euronews.com/euronews/en/world", "category": "general"},
    "Deutsche Welle": {"url": "https://rss.dw.com/rdf/rss-de-all", "category": "general"},
}

IRAN_KEYWORDS = [
    "iran", "iranian", "tehran", "persian gulf", "nuclear", "sanctions",
    "revolutionary guard", "hormuz", "oil", "uranium", "deal", "jcpoa",
    "middle east", "gulf", "saudi", "israel", "usa", "trump", "biden",
    "military", "war", "attack", "missile", "drone", "navy", "tanker", "ship"
]

TAG_KEYWORDS = {
    "هرمز": ["hormuz", "strait", "tanker", "ship", "navy", "naval"],
    "نظامی": ["military", "army", "soldier", "missile", "drone", "weapon", "war"],
    "سیاسی": ["political", "diplomat", "meeting", "summit", "negotiat", "agreement"],
    "اقتصادی": ["economy", "oil", "sanction", "trade", "market", "currency"],
    "هسته‌ای": ["nuclear", "uranium", "enrichment", "atomic", "reactor"],
    "تحریم": ["sanction", "ban", "restrict", "penalty"],
    "دریایی": ["navy", "ship", "vessel", "maritime", "sea", "ocean"],
    "خاورمیانه": ["middle east", "gulf", "saudi", "israel", "lebanon", "syria", "iraq"]
}

URGENCY_KEYWORDS = {
    "high": ["breaking", "urgent", "attack", "war", "explosion", "crisis", "emergency", "killed", "death"],
    "medium": ["tension", "threat", "warning", "sanctions", "nuclear", "military"],
    "low": ["trade", "economy", "cultural", "sport", "science"]
}

SENTIMENT_KEYWORDS = {
    "negative": ["war", "attack", "killed", "death", "threat", "crisis", "conflict", "tension", "sanctions"],
    "positive": ["peace", "deal", "agreement", "cooperation", "trade", "growth", "success"]
}
