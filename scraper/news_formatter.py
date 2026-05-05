"""
ماژول فرمت‌دهی و ترجمه اخبار - با قالب دقیق JSON شما
"""

from typing import List, Dict
import json
import time


class NewsFormatter:
    def __init__(self):
        self.translated_cache = {}
    
    def translate_text(self, text: str, target: str = 'fa') -> str:
        """ترجمه متن"""
        if not text or text.strip() == '':
            return ''
        
        cache_key = f"{text}_{target}"
        if cache_key in self.translated_cache:
            return self.translated_cache[cache_key]
        
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, dest=target)
            translated = result.text
            self.translated_cache[cache_key] = translated
            time.sleep(0.5)
            return translated
        except Exception as e:
            print(f"   ⚠️ خطا در ترجمه: {e}")
            return text
    
    def generate_summary_points(self, article: Dict) -> List[str]:
        """تولید نکات کلیدی"""
        points = []
        
        if article.get('title_en'):
            points.append(f"خبر اصلی: {article['title_en']}")
        
        if article.get('source'):
            points.append(f"این خبر از منبع {article['source']} گزارش شده است.")
        
        urgency = article.get('urgency', 5)
        if urgency >= 7:
            points.append("این خبر دارای فوریت بالایی است و نیاز به توجه فوری دارد.")
        elif urgency >= 4:
            points.append("این خبر دارای اهمیت متوسطی است.")
        
        sentiment = article.get('sentiment', 0)
        if sentiment < -0.3:
            points.append("محتوای این خبر منفی است و می‌تواند تأثیرات نامطلوبی داشته باشد.")
        elif sentiment > 0.3:
            points.append("محتوای این خبر مثبت ارزیابی می‌شود.")
        
        return points[:3]
    
    def generate_impact(self, article: Dict) -> str:
        """تولید متن تأثیر خبر"""
        urgency = article.get('urgency', 5)
        sentiment = article.get('sentiment', 0)
        tag = article.get('tag', 'عمومی')
        
        if urgency >= 8:
            impact = f"این خبر با فوریت بسیار بالا می‌تواند تأثیرات جدی بر وضعیت {tag} داشته باشد. "
        elif urgency >= 5:
            impact = f"این خبر می‌تواند تأثیرات قابل توجهی بر رویدادهای {tag} داشته باشد. "
        else:
            impact = f"این خبر تأثیر محدودی بر وضعیت {tag} دارد. "
        
        if sentiment < -0.5:
            impact += "لزوم پایش دقیق وضعیت توصیه می‌شود."
        elif sentiment > 0.5:
            impact += "این تحولات می‌تواند نتایج مثبتی به همراه داشته باشد."
        else:
            impact += "توصیه می‌شود وضعیت پایش شود."
        
        return impact
    
    def format_articles(self, translate: bool = True):
        """فرمت‌دهی و ترجمه اخبار"""
        print("\n🔄 در حال فرمت‌دهی و ترجمه اخبار...\n")
        
        # خواندن فایل
        with open('news.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        formatted = []
        
        for i, article in enumerate(articles):
            print(f"   پردازش {i+1}/{len(articles)}: {article['title_en'][:50]}...")
            
            # ترجمه title_fa
            if translate and not article.get('title_fa'):
                article['title_fa'] = self.translate_text(article['title_en'])
            
            # تولید خلاصه‌های جدید
            article['summary'] = self.generate_summary_points(article)
            
            # تولید impact
            article['impact'] = self.generate_impact(article)
            
            formatted.append(article)
        
        # ذخیره با قالب دقیق (آرایه ساده)
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(formatted, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {len(formatted)} خبر فرمت‌دهی و ذخیره شد")


if __name__ == "__main__":
    formatter = NewsFormatter()
    formatter.format_articles(translate=True)
