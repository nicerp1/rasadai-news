"""
ماژول جمع‌آوری اخبار از منابع مختلف
"""
import feedparser
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import json
import sys
import os

# اضافه کردن مسیر فعلی به مسیر ماژول‌ها
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import RSS_FEEDS, IRAN_KEYWORDS, TAG_KEYWORDS, URGENCY_KEYWORDS, SENTIMENT_KEYWORDS
except ImportError:
    print("خطا: فایل config.py یافت نشد. لطفاً مطمئن شوید فایل config.py در کنار scraper.py است.")
    sys.exit(1)

class NewsScraper:
    # اصلاح ۱: دو آندرلاین در ابتدا و انتهای init
    def __init__(self):
        self.articles = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def is_iran_related(self, title: str, summary: str = "") -> bool:
        """بررسی مرتبط بودن خبر با ایران"""
        text = (title + " " + summary).lower()
        return any(keyword.lower() in text for keyword in IRAN_KEYWORDS)

    def clean_html(self, html: str) -> str:
        """پاکسازی تگ‌های HTML"""
        if not html:
            return ""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except Exception:
            return html

    def extract_image(self, entry) -> Optional[str]:
        """استخراج تصویر از خبر"""
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if 'url' in media:
                    return media['url']
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image'):
                    return enclosure.get('url')
        if hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('image'):
                    return link.get('href')
        return None

    def parse_date(self, date_str: str) -> float:
        """تبدیل تاریخ به timestamp"""
        if not date_str:
            return datetime.now().timestamp()
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%d %b %Y %H:%M:%S',
        ]
        for fmt in formats:
            try:
                # اصلاح کوچک برای هندل کردن Z
                clean_date = date_str.replace('Z', '+0000')
                dt = datetime.strptime(clean_date, fmt)
                return dt.timestamp()
            except:
                continue
        return datetime.now().timestamp()

    def scrape_feed(self, source_name: str, feed_info: Dict) -> List[Dict]:
        """جمع‌آوری اخبار از یک فید RSS"""
        articles = []
        try:
            print(f"📡 در حال جمع‌آوری از {source_name}...")
            feed = feedparser.parse(feed_info['url'])
            for entry in feed.entries[:15]:
                title = self.clean_html(entry.get('title', ''))
                link = entry.get('link', '')
                if '?oc=' in link:
                    link = link.split('?oc=')[0]
                summary = self.clean_html(entry.get('summary', entry.get('description', '')))
                
                if not self.is_iran_related(title, summary):
                    continue
                
                article = {
                    "title_fa": "",
                    "title_en": title,
                    "summary": [summary] if summary else [],
                    "impact": "",
                    "tag": self.detect_tag(title + ' ' + summary),
                    "urgency": self.calculate_urgency(title, summary),
                    "sentiment": self.calculate_sentiment(title, summary),
                    "source": source_name,
                    "url": link,
                    "clean_url": link,
                    "image": self.extract_image(entry),
                    "timestamp": self.parse_date(entry.get('published', ''))
                }
                articles.append(article)
            print(f"   ✅ {len(articles)} خبر مرتبط از {source_name}")
        except Exception as e:
            print(f"   ❌ خطا در {source_name}: {e}")
        time.sleep(1)
        return articles

    def detect_tag(self, text: str) -> str:
        """تشخیص تگ خبر"""
        text_lower = text.lower()
        for tag, keywords in TAG_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                return tag
        return "عمومی"

    def calculate_urgency(self, title: str, summary: str) -> int:
        """محاسبه فوریت خبر"""
        text = (title + " " + summary).lower()
        score = 5
        high_keywords = URGENCY_KEYWORDS.get('high', [])
        medium_keywords = URGENCY_KEYWORDS.get('medium', [])
        
        for keyword in high_keywords:
            if keyword.lower() in text:
                score += 3
        for keyword in medium_keywords:
            if keyword.lower() in text:
                score += 1
        return min(10, max(1, score))

    def calculate_sentiment(self, title: str, summary: str) -> float:
        """محاسبه احساس خبر"""
        text = (title + " " + summary).lower()
        negative_keywords = SENTIMENT_KEYWORDS.get('negative', [])
        positive_keywords = SENTIMENT_KEYWORDS.get('positive', [])
        
        negative_count = sum(1 for kw in negative_keywords if kw.lower() in text)
        positive_count = sum(1 for kw in positive_keywords if kw.lower() in text)
        
        if negative_count > positive_count:
            return -0.7
        elif positive_count > negative_count:
            return 0.7
        return 0.0

    def scrape_all(self) -> List[Dict]:
        """جمع‌آوری از همه منابع"""
        print("🚀 شروع جمع‌آوری اخبار...\n")
        for source_name, feed_info in RSS_FEEDS.items():
            articles = self.scrape_feed(source_name, feed_info)
            self.articles.extend(articles)
        
        # حذف تکراری‌ها
        seen_urls = set()
        unique_articles = []
        for article in self.articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        # مرتب‌سازی بر اساس زمان
        unique_articles.sort(key=lambda x: x['timestamp'], reverse=True)
        
        print(f"\n📊 جمعاً {len(unique_articles)} خبر یکتا جمع‌آوری شد")
        
        # ذخیره با قالب دقیق JSON شما (آرایه ساده)
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(unique_articles, f, ensure_ascii=False, indent=2)
        
        print("💾 فایل news.json ذخیره شد")
        return unique_articles

# اصلاح ۲: دو آندرلاین در ابتدا و انتهای name
if __name__ == "__main__":
    scraper = NewsScraper()
    articles = scraper.scrape_all()
    print(f"\n✅ عملیات با موفقیت انجام شد!")
