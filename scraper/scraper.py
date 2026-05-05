"""
ماژول جمع‌آوری اخبار
"""

import feedparser
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time
import json

from config import RSS_FEEDS, IRAN_KEYWORDS


class NewsScraper:
    def __init__(self):
        self.articles = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def is_iran_related(self, title: str, summary: str = "") -> bool:
        text = (title + " " + summary).lower()
        return any(keyword.lower() in text for keyword in IRAN_KEYWORDS)
    
    def clean_html(self, html: str) -> str:
        if not html:
            return ""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    
    def extract_image(self, entry) -> Optional[str]:
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
        if not date_str:
            return datetime.now().timestamp()
        formats = ['%a, %d %b %Y %H:%M:%S %z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S']
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str.replace('Z', '+0000'), fmt)
                return dt.timestamp()
            except:
                continue
        return datetime.now().timestamp()
    
    def scrape_feed(self, source_name: str, feed_info: Dict) -> List[Dict]:
        articles = []
        try:
            print(f"📡 {
