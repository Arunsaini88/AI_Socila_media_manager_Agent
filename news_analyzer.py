# news_analyzer.py
import requests
from bs4 import BeautifulSoup
import feedparser
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
import re
from urllib.parse import quote_plus, urlencode

class NewsAnalyzer:
    """Analyzes industry news and trends to provide content insights"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Industry-specific news sources and RSS feeds
        self.news_sources = {
            'fitness': {
                'rss_feeds': [
                    'https://www.fitnessmagazine.com/rss.xml',
                    'https://www.menshealth.com/rss/all.xml'
                ],
                'keywords': ['fitness', 'workout', 'gym', 'health', 'exercise', 'training'],
                'mock_headlines': [
                    "New HIIT workout trends gaining popularity in 2025",
                    "Wearable fitness tech sees 40% growth this quarter",
                    "Mental health benefits of regular exercise confirmed in latest study",
                    "Virtual personal training becomes mainstream post-pandemic",
                    "Nutrition timing: When to eat for optimal workout performance"
                ]
            },
            'beauty': {
                'rss_feeds': [
                    'https://www.allure.com/feed/rss',
                    'https://www.harpersbazaar.com/rss/all.xml'
                ],
                'keywords': ['beauty', 'skincare', 'cosmetics', 'hair', 'makeup', 'spa'],
                'mock_headlines': [
                    "Clean beauty movement drives 60% of new product launches",
                    "K-beauty trends continue to influence global market",
                    "Sustainable packaging becomes priority for beauty brands",
                    "At-home beauty treatments market expected to double",
                    "Anti-aging serums with peptides show promising results"
                ]
            },
            'food': {
                'rss_feeds': [
                    'https://www.foodnetwork.com/feeds/all.rss',
                    'https://www.bonappetit.com/feed/rss'
                ],
                'keywords': ['restaurant', 'food', 'dining', 'culinary', 'cuisine', 'chef'],
                'mock_headlines': [
                    "Plant-based menu options now standard in 75% of restaurants",
                    "Ghost kitchens reshape food delivery landscape",
                    "Sustainable sourcing becomes key differentiator",
                    "Local ingredients trend drives menu innovation",
                    "Technology transforms restaurant customer experience"
                ]
            },
            'retail': {
                'rss_feeds': [
                    'https://nrf.com/feed',
                    'https://www.retaildive.com/feeds/news/'
                ],
                'keywords': ['retail', 'shopping', 'ecommerce', 'fashion', 'store'],
                'mock_headlines': [
                    "Omnichannel retail strategies show 35% higher customer retention",
                    "AR try-on technology adoption accelerates across fashion brands",
                    "Sustainable fashion drives purchasing decisions for Gen Z",
                    "Local shopping experiences make comeback",
                    "Inventory management AI reduces waste by 45%"
                ]
            },
            'healthcare': {
                'rss_feeds': [
                    'https://www.healthcarefinancenews.com/feeds/all.rss'
                ],
                'keywords': ['healthcare', 'medical', 'wellness', 'health', 'treatment'],
                'mock_headlines': [
                    "Telemedicine adoption remains high post-pandemic",
                    "Preventive care focus reduces long-term healthcare costs",
                    "Wearable health monitoring devices gain medical approval",
                    "Mental health services see increased demand and innovation",
                    "Personalized medicine approaches show promising outcomes"
                ]
            },
            'general': {
                'rss_feeds': [
                    'https://feeds.feedburner.com/TechCrunch'
                ],
                'keywords': ['business', 'technology', 'innovation', 'trends'],
                'mock_headlines': [
                    "Small businesses embrace digital transformation",
                    "Customer experience becomes top business priority",
                    "AI tools help small businesses compete with larger companies",
                    "Social media marketing ROI reaches all-time high",
                    "Local business support drives community economic growth"
                ]
            }
        }
        
        # Google News search base URL (for scraping)
        self.google_news_base = "https://news.google.com/rss/search"
    
    def get_industry_news(self, industry: str, keywords: List[str] = None, limit: int = 5) -> List[Dict]:
        """
        Get current industry news and insights
        
        Args:
            industry: Industry category (e.g., 'fitness', 'beauty', 'food')
            keywords: Additional keywords to search for
            limit: Number of news items to return (default 5)
            
        Returns:
            List of news items with headlines, summaries, and insights
        """
        industry = industry.lower()
        
        # Get industry configuration
        industry_config = self.news_sources.get(industry, self.news_sources['general'])
        
        # Combine keywords
        all_keywords = industry_config['keywords'][:]
        if keywords:
            all_keywords.extend(keywords)
        
        news_items = []
        
        try:
            # Try to get real news from RSS feeds
            rss_news = self._get_rss_news(industry_config['rss_feeds'], all_keywords, limit//2)
            news_items.extend(rss_news)
            
            # Try Google News search
            google_news = self._get_google_news(all_keywords, limit//2)
            news_items.extend(google_news)
            
        except Exception as e:
            print(f"Error fetching real news: {e}")
        
        # If we don't have enough real news, supplement with mock data
        if len(news_items) < limit:
            mock_news = self._get_mock_news(industry_config, limit - len(news_items))
            news_items.extend(mock_news)
        
        # Ensure we don't exceed the limit
        news_items = news_items[:limit]
        
        # Add insights and business relevance
        for item in news_items:
            item['business_insights'] = self._generate_business_insights(item, industry)
            item['content_ideas'] = self._generate_content_ideas(item, industry)
        
        return news_items
    
    def _get_rss_news(self, rss_feeds: List[str], keywords: List[str], limit: int) -> List[Dict]:
        """Fetch news from RSS feeds"""
        news_items = []
        
        for feed_url in rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:limit]:
                    # Check if entry is relevant to keywords
                    text_to_check = (entry.title + ' ' + entry.get('summary', '')).lower()
                    if any(keyword.lower() in text_to_check for keyword in keywords):
                        
                        news_item = {
                            'headline': entry.title,
                            'summary': entry.get('summary', '')[:200] + '...' if len(entry.get('summary', '')) > 200 else entry.get('summary', ''),
                            'url': entry.link,
                            'published_date': entry.get('published', ''),
                            'source': feed.feed.get('title', 'Unknown'),
                            'type': 'rss'
                        }
                        news_items.append(news_item)
                        
                        if len(news_items) >= limit:
                            break
                            
            except Exception as e:
                print(f"Error parsing RSS feed {feed_url}: {e}")
                continue
        
        return news_items
    
    def _get_google_news(self, keywords: List[str], limit: int) -> List[Dict]:
        """Fetch news from Google News search"""
        news_items = []
        
        try:
            # Create search query - properly encode spaces and special characters
            query = ' OR '.join(keywords[:3])  # Use top 3 keywords
            
            # Properly encode the query parameters
            params = {
                'q': query,
                'hl': 'en-US',
                'gl': 'US',
                'ceid': 'US:en'
            }
            
            # Build the URL with proper encoding
            url = f"{self.google_news_base}?{urlencode(params)}"
            
            print(f"Fetching Google News from: {url}")  # Debug log
            
            # Parse the RSS feed
            feed = feedparser.parse(url)
            
            if not feed.entries:
                print("No entries found in Google News feed")
                return news_items
            
            for entry in feed.entries[:limit]:
                # Clean up the title (remove source suffix if present)
                title = entry.title
                if ' - ' in title:
                    title = title.rsplit(' - ', 1)[0]
                
                news_item = {
                    'headline': title,
                    'summary': entry.get('summary', '')[:200] + '...' if len(entry.get('summary', '')) > 200 else entry.get('summary', ''),
                    'url': entry.link,
                    'published_date': entry.get('published', ''),
                    'source': 'Google News',
                    'type': 'google_news'
                }
                news_items.append(news_item)
                
        except Exception as e:
            print(f"Error fetching Google News: {e}")
        
        return news_items
    
    def _get_mock_news(self, industry_config: Dict, limit: int) -> List[Dict]:
        """Generate mock news items for testing and fallback"""
        mock_headlines = industry_config['mock_headlines']
        news_items = []
        
        for i, headline in enumerate(mock_headlines[:limit]):
            news_item = {
                'headline': headline,
                'summary': f"Industry analysis shows significant trends in {headline.lower()}. This development could impact local businesses in various ways.",
                'url': f"https://example-news.com/article/{i+1}",
                'published_date': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                'source': 'Industry Reports',
                'type': 'mock'
            }
            news_items.append(news_item)
        
        return news_items
    
    def _generate_business_insights(self, news_item: Dict, industry: str) -> List[str]:
        """Generate business insights from news item"""
        headline = news_item['headline'].lower()
        insights = []
        
        # Generic insights based on common news patterns
        if 'trend' in headline or 'popular' in headline:
            insights.append("Consider incorporating this trend into your service offerings")
            insights.append("Update your marketing messaging to align with current trends")
        
        if 'technology' in headline or 'digital' in headline:
            insights.append("Evaluate how this technology could improve your business operations")
            insights.append("Consider digital adoption to stay competitive")
        
        if 'customer' in headline or 'consumer' in headline:
            insights.append("Review your customer experience strategy")
            insights.append("Adapt services to meet changing customer expectations")
        
        if 'growth' in headline or 'increase' in headline:
            insights.append("This presents a potential business opportunity")
            insights.append("Consider expanding services in this area")
        
        # Industry-specific insights
        if industry == 'fitness':
            if 'workout' in headline:
                insights.append("Update your class schedule to include trending workout styles")
            if 'nutrition' in headline:
                insights.append("Consider partnering with nutritionists or offering meal plans")
        
        elif industry == 'beauty':
            if 'skincare' in headline:
                insights.append("Review your skincare service menu for new treatment options")
            if 'sustainable' in headline:
                insights.append("Highlight eco-friendly products and practices")
        
        elif industry == 'food':
            if 'plant-based' in headline:
                insights.append("Expand plant-based options on your menu")
            if 'local' in headline:
                insights.append("Emphasize local sourcing in your marketing")
        
        # Ensure we have at least some insights
        if not insights:
            insights = [
                "Monitor this trend for potential business impact",
                "Consider how this development affects your target market"
            ]
        
        return insights[:3]  # Limit to 3 insights
    
    def _generate_content_ideas(self, news_item: Dict, industry: str) -> List[str]:
        """Generate social media content ideas based on news item"""
        headline = news_item['headline']
        content_ideas = []
        
        # Generic content ideas
        content_ideas.extend([
            f"Share your thoughts on: {headline}",
            f"How this trend affects our clients: {headline}",
            f"Behind the scenes: How we're adapting to {headline.lower()}"
        ])
        
        # Industry-specific content ideas
        if industry == 'fitness':
            content_ideas.extend([
                "Post a workout video demonstrating the trending exercise",
                "Share client transformation stories related to this trend",
                "Create an educational post about the health benefits"
            ])
        
        elif industry == 'beauty':
            content_ideas.extend([
                "Before/after photos showcasing relevant treatments",
                "Tutorial video demonstrating trending techniques",
                "Product recommendation post featuring trending items"
            ])
        
        elif industry == 'food':
            content_ideas.extend([
                "Share photos of dishes that align with this trend",
                "Post about your restaurant's take on trending cuisine",
                "Behind-the-scenes video of food preparation"
            ])
        
        return content_ideas[:4]  # Limit to 4 content ideas
    
    def get_seasonal_trends(self, industry: str) -> List[Dict]:
        """Get seasonal trends relevant to the industry"""
        current_month = datetime.now().month
        seasonal_trends = []
        
        # Define seasonal trends by industry
        seasonal_data = {
            'fitness': {
                1: ["New Year fitness resolutions", "Detox and cleanse programs"],
                3: ["Spring cleaning workouts", "Outdoor fitness preparation"],
                6: ["Summer body preparation", "Beach workout routines"],
                9: ["Back-to-school fitness schedules", "Fall sports training"],
                12: ["Holiday stress relief workouts", "Winter fitness motivation"]
            },
            'beauty': {
                1: ["New year skincare routines", "Post-holiday skin recovery"],
                3: ["Spring skincare transition", "Allergy-season skin prep"],
                6: ["Summer sun protection", "Vacation-ready beauty"],
                9: ["Fall skincare adjustment", "Back-to-school beauty prep"],
                12: ["Holiday glam services", "Winter skin hydration"]
            },
            'food': {
                1: ["Healthy eating resolutions", "Detox menu items"],
                3: ["Spring fresh ingredients", "Easter brunch specials"],
                6: ["Summer BBQ options", "Fresh summer salads"],
                9: ["Comfort food season", "Harvest ingredient menus"],
                12: ["Holiday catering", "New Year's Eve dining"]
            }
        }
        
        industry_trends = seasonal_data.get(industry, {})
        month_trends = industry_trends.get(current_month, ["Seasonal business opportunities"])
        
        for trend in month_trends:
            seasonal_trends.append({
                'trend': trend,
                'relevance': 'high',
                'timeframe': 'current_month',
                'content_potential': 'high'
            })
        
        return seasonal_trends

# Test function
def test_news_analyzer():
    """Test the news analyzer"""
    analyzer = NewsAnalyzer()
    
    # Test different industries
    industries = ['fitness', 'beauty', 'food', 'general']
    
    for industry in industries:
        print(f"\n=== Testing {industry.upper()} News ===")
        news = analyzer.get_industry_news(industry, limit=3)
        
        for item in news:
            print(f"Headline: {item['headline']}")
            print(f"Source: {item['source']}")
            print(f"Insights: {item['business_insights']}")
            print(f"Content Ideas: {item['content_ideas']}")
            print("-" * 40)

if __name__ == "__main__":
    test_news_analyzer()