# business_analyzer.py
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Optional
import json

class BusinessAnalyzer:
    """Analyzes business websites to extract structured business profiles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Industry keywords for classification
        self.industry_keywords = {
            'fitness': ['gym', 'fitness', 'workout', 'training', 'exercise', 'health club', 'personal trainer'],
            'beauty': ['salon', 'spa', 'beauty', 'hair', 'nail', 'massage', 'facial', 'cosmetic'],
            'food': ['restaurant', 'cafe', 'coffee', 'dining', 'food', 'bakery', 'catering', 'bistro'],
            'retail': ['shop', 'store', 'boutique', 'retail', 'fashion', 'clothing', 'accessories'],
            'healthcare': ['medical', 'dental', 'clinic', 'doctor', 'healthcare', 'therapy', 'wellness'],
            'education': ['school', 'academy', 'training', 'education', 'learning', 'course', 'tutor'],
            'professional': ['consulting', 'legal', 'accounting', 'financial', 'insurance', 'real estate'],
            'automotive': ['auto', 'car', 'garage', 'mechanic', 'repair', 'dealership', 'vehicle'],
            'entertainment': ['entertainment', 'event', 'party', 'music', 'venue', 'club', 'theater']
        }
        
        # Tone indicators
        self.tone_indicators = {
            'professional': ['expert', 'professional', 'certified', 'licensed', 'quality', 'experience'],
            'friendly': ['friendly', 'welcome', 'family', 'community', 'caring', 'personal', 'warm'],
            'casual': ['fun', 'easy', 'simple', 'relaxed', 'comfortable', 'laid-back', 'chill'],
            'premium': ['luxury', 'premium', 'exclusive', 'high-end', 'elite', 'sophisticated', 'upscale']
        }
    
    def analyze_website(self, url: str) -> Dict:
        """
        Analyze a business website and extract structured profile
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Dict containing business profile information
        """
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Scrape website content
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            business_name = self._extract_business_name(soup, url)
            description = self._extract_description(soup)
            services = self._extract_services(soup)
            contact_info = self._extract_contact_info(soup)
            
            # Analyze industry and tone
            full_text = soup.get_text().lower()
            industry = self._classify_industry(full_text, services)
            tone = self._analyze_tone(full_text)
            
            # Extract social proof
            social_proof = self._extract_social_proof(soup)
            
            profile = {
                'business_name': business_name,
                'website_url': url,
                'industry': industry,
                'description': description,
                'services': services,
                'tone_of_voice': tone,
                'contact_info': contact_info,
                'social_proof': social_proof,
                'extracted_at': self._get_timestamp()
            }
            
            return profile
            
        except Exception as e:
            # Return fallback profile with error info
            return {
                'business_name': self._extract_domain_name(url),
                'website_url': url,
                'industry': 'general',
                'description': 'Business profile could not be fully extracted',
                'services': [],
                'tone_of_voice': 'professional',
                'contact_info': {},
                'social_proof': {},
                'error': str(e),
                'extracted_at': self._get_timestamp()
            }
    
    def _extract_business_name(self, soup: BeautifulSoup, url: str) -> str:
        """Extract business name from various sources"""
        # Try title tag
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            # Clean up common title patterns
            name = re.sub(r'\s*[\|\-\—]\s*.*$', '', title_text)
            if name and len(name) > 2:
                return name
        
        # Try h1 tags
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text().strip()
            if text and len(text) < 100:  # Reasonable business name length
                return text
        
        # Try meta property og:site_name
        og_site_name = soup.find('meta', property='og:site_name')
        if og_site_name and og_site_name.get('content'):
            return og_site_name['content']
        
        # Fallback to domain name
        return self._extract_domain_name(url)
    
    def _extract_domain_name(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            domain = urlparse(url).netloc
            return domain.replace('www.', '').split('.')[0].title()
        except:
            return 'Business'
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract business description"""
        # Try meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # Try og:description
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        # Try to find description in common sections
        selectors = [
            '.about', '.description', '.intro', '.hero-text',
            '#about', '#description', '.welcome', '.mission'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                if 50 < len(text) < 500:  # Reasonable description length
                    return text
        
        # Try first few paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs[:3]:
            text = p.get_text().strip()
            if 30 < len(text) < 300:
                return text
        
        return "No description available"
    
    def _extract_services(self, soup: BeautifulSoup) -> List[str]:
        """Extract services offered by the business"""
        services = set()
        
        # Look for service-related sections
        service_selectors = [
            '.services', '.service', '.offerings', '.products',
            '#services', '#service', '.menu', '.treatments'
        ]
        
        for selector in service_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Extract text from list items
                list_items = element.find_all(['li', 'h3', 'h4', 'h5'])
                for item in list_items:
                    text = item.get_text().strip()
                    if 5 < len(text) < 100:  # Reasonable service name length
                        services.add(text)
        
        # Look for common service keywords in headings
        headings = soup.find_all(['h2', 'h3', 'h4'])
        for heading in headings:
            text = heading.get_text().strip().lower()
            if any(keyword in text for keyword in ['service', 'offer', 'provide', 'specialize']):
                services.add(heading.get_text().strip())
        
        return list(services)[:10]  # Limit to 10 services
    
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contact_info = {}
        
        # Extract phone numbers
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        text_content = soup.get_text()
        phone_matches = re.findall(phone_pattern, text_content)
        if phone_matches:
            contact_info['phone'] = ''.join(phone_matches[0])
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, text_content)
        if email_matches:
            contact_info['email'] = email_matches[0]
        
        # Extract address (simplified)
        address_selectors = ['.address', '.location', '.contact-address', '#address']
        for selector in address_selectors:
            element = soup.select_one(selector)
            if element:
                address_text = element.get_text().strip()
                if len(address_text) > 10:
                    contact_info['address'] = address_text
                    break
        
        return contact_info
    
    def _classify_industry(self, text: str, services: List[str]) -> str:
        """Classify business industry based on content"""
        all_text = text + ' ' + ' '.join(services).lower()
        
        industry_scores = {}
        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores, key=industry_scores.get)
        
        return 'general'
    
    def _analyze_tone(self, text: str) -> str:
        """Analyze tone of voice from website content"""
        tone_scores = {}
        
        for tone, keywords in self.tone_indicators.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                tone_scores[tone] = score
        
        if tone_scores:
            return max(tone_scores, key=tone_scores.get)
        
        return 'professional'  # Default tone
    
    def _extract_social_proof(self, soup: BeautifulSoup) -> Dict:
        """Extract social proof elements like reviews, testimonials"""
        social_proof = {}
        
        # Look for review/rating information
        rating_selectors = ['.rating', '.stars', '.review-rating', '.score']
        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                # Try to extract numerical rating
                rating_match = re.search(r'(\d+\.?\d*)', text)
                if rating_match:
                    social_proof['rating'] = rating_match.group(1)
        
        # Count testimonials
        testimonial_selectors = ['.testimonial', '.review', '.feedback', '.client-review']
        testimonial_count = 0
        for selector in testimonial_selectors:
            testimonial_count += len(soup.select(selector))
        
        if testimonial_count > 0:
            social_proof['testimonials_count'] = testimonial_count
        
        # Look for client logos or mentions
        client_selectors = ['.clients', '.partners', '.featured-in', '.logos']
        for selector in client_selectors:
            element = soup.select_one(selector)
            if element:
                social_proof['has_client_logos'] = True
                break
        
        return social_proof
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Test function
def test_business_analyzer():
    """Test the business analyzer with sample websites"""
    analyzer = BusinessAnalyzer()
    
    # Test with various business types
    test_urls = [
        'https://example-gym.com',  # Would need real URLs for testing
        'https://example-salon.com',
        'https://example-restaurant.com'
    ]
    
    for url in test_urls:
        try:
            profile = analyzer.analyze_website(url)
            print(f"Profile for {url}:")
            print(json.dumps(profile, indent=2))
            print("-" * 50)
        except Exception as e:
            print(f"Error analyzing {url}: {e}")

if __name__ == "__main__":
    test_business_analyzer()