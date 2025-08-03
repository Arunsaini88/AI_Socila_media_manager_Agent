# content_generator.py
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

class ContentGenerator:
    """Generates Facebook post content based on business profiles and industry insights"""
    
    def __init__(self):
        # Post templates by type and tone
        self.post_templates = {
            'promo': {
                'professional': [
                    "We're excited to announce {offer}! {business_name} is committed to providing {value_prop}. {call_to_action} {contact_info}",
                    "Limited time offer: {offer}. Experience the {business_name} difference. {call_to_action}",
                    "Special promotion alert! {offer} at {business_name}. {value_prop} {call_to_action}"
                ],
                'friendly': [
                    "Hey everyone! 🎉 We've got something special for you: {offer}! Come see us at {business_name} and {value_prop}. {call_to_action}",
                    "Guess what? {offer} is here! 😊 We can't wait to see you at {business_name}. {call_to_action}",
                    "Friends, we're so excited to share {offer} with you! {business_name} is all about {value_prop}. {call_to_action}"
                ],
                'casual': [
                    "Yo! {offer} just dropped! 🔥 Come through {business_name} and check it out. {call_to_action}",
                    "New deal alert! {offer} - because you deserve the best. {call_to_action}",
                    "PSA: {offer} is happening now! Don't sleep on this one. {call_to_action}"
                ],
                'premium': [
                    "Exclusive opportunity: {offer}. Discover the luxury experience at {business_name}. {value_prop} {call_to_action}",
                    "Elevate your experience with {offer}. {business_name} - where excellence meets sophistication. {call_to_action}",
                    "Premium members, this is for you: {offer}. Experience unparalleled {value_prop} at {business_name}."
                ]
            },
            'tip': {
                'professional': [
                    "Professional tip: {tip_content}. At {business_name}, we believe in sharing knowledge to help you {benefit}. {call_to_action}",
                    "Industry insight: {tip_content} This is why at {business_name}, we focus on {value_prop}. {call_to_action}",
                    "Expert advice: {tip_content} Trust {business_name} for professional {industry} guidance."
                ],
                'friendly': [
                    "Quick tip from your friends at {business_name}: {tip_content} 💡 We love helping you {benefit}! {call_to_action}",
                    "Here's something helpful: {tip_content} ✨ That's just one way we care for our {business_name} family! {call_to_action}",
                    "Friendly reminder: {tip_content} 😊 We're always here to help at {business_name}!"
                ],
                'casual': [
                    "Pro tip: {tip_content} 💯 That's the kind of real talk you get from {business_name}. {call_to_action}",
                    "Life hack: {tip_content} You're welcome! 😎 More tips coming from your crew at {business_name}.",
                    "Real talk: {tip_content} That's how we roll at {business_name}. {call_to_action}"
                ],
                'premium': [
                    "Expert insight: {tip_content} This level of expertise is what distinguishes {business_name}. {call_to_action}",
                    "Exclusive knowledge: {tip_content} Elevate your {industry} experience with {business_name}.",
                    "Professional mastery: {tip_content} Discover the {business_name} advantage."
                ]
            },
            'update': {
                'professional': [
                    "Update from {business_name}: {update_content}. We're committed to {value_prop} and keeping you informed. {call_to_action}",
                    "Business update: {update_content} Thank you for your continued trust in {business_name}. {call_to_action}",
                    "Important notice: {update_content} {business_name} remains dedicated to serving you with excellence."
                ],
                'friendly': [
                    "Hey everyone! Quick update from the {business_name} family: {update_content} 😊 {call_to_action}",
                    "Update time! {update_content} Thanks for being part of the {business_name} community! 💙 {call_to_action}",
                    "Just wanted to let you know: {update_content} Love you all! - The {business_name} team ❤️"
                ],
                'casual': [
                    "What's up! Quick update: {update_content} Keep doing you! 🤘 - {business_name}",
                    "Update drop: {update_content} Thanks for rolling with us! 🔥 {call_to_action}",
                    "Heads up: {update_content} Much love from {business_name}! ✌️"
                ],
                'premium': [
                    "Exclusive update for our valued clients: {update_content} {business_name} continues to set the standard for excellence.",
                    "Important announcement: {update_content} Your luxury experience at {business_name} remains our priority.",
                    "Distinguished clients, please note: {update_content} {business_name} - your premier destination."
                ]
            },
            'insight': {
                'professional': [
                    "Industry insight: {insight_content} At {business_name}, we stay ahead of trends to better serve you. {call_to_action}",
                    "Market analysis: {insight_content} This is why choosing {business_name} makes a difference. {call_to_action}",
                    "Professional perspective: {insight_content} Trust {business_name} to keep you informed and ahead."
                ],
                'friendly': [
                    "Interesting news! {insight_content} 🤓 We love staying on top of trends for our {business_name} family! {call_to_action}",
                    "Did you know? {insight_content} ✨ That's why we're always evolving at {business_name}! {call_to_action}",
                    "Cool industry update: {insight_content} 😎 We're always learning for you at {business_name}!"
                ],
                'casual': [
                    "FYI: {insight_content} 📰 That's why {business_name} stays fresh and relevant! {call_to_action}",
                    "Industry tea: {insight_content} ☕ We keep our finger on the pulse at {business_name}!",
                    "Real industry talk: {insight_content} 💯 {business_name} keeps it 100 with the latest!"
                ],
                'premium': [
                    "Market intelligence: {insight_content} {business_name} leverages industry insights for your advantage.",
                    "Exclusive industry analysis: {insight_content} Discover how {business_name} stays at the forefront.",
                    "Strategic insight: {insight_content} {business_name} - where expertise meets innovation."
                ]
            }
        }
        
        # Industry-specific content elements
        self.industry_content = {
            'fitness': {
                'offers': [
                    "50% off personal training sessions this month",
                    "Free fitness assessment with membership signup",
                    "Buy 10 classes, get 2 free",
                    "New member special: First month for $39",
                    "Partner workout packages available"
                ],
                'tips': [
                    "Stay hydrated - aim for 8 glasses of water daily",
                    "Warm up before workouts to prevent injury",
                    "Rest days are just as important as workout days",
                    "Focus on form over speed for better results",
                    "Set realistic goals and celebrate small wins"
                ],
                'value_props': [
                    "helping you achieve your fitness goals",
                    "creating a supportive fitness community",
                    "providing expert guidance and motivation",
                    "offering flexible workout options",
                    "building healthy lifestyle habits"
                ],
                'hashtags': ['#fitness', '#gym', '#workout', '#health', '#motivation', '#personaltraining', '#fitnesscommunity']
            },
            'beauty': {
                'offers': [
                    "20% off all facial treatments this week",
                    "Bridal package deal - hair, makeup, and nails",
                    "Refer a friend and both get 15% off",
                    "New client special: $99 spa day package",
                    "Loyalty program: 10th service free"
                ],
                'tips': [
                    "Always remove makeup before bed",
                    "Use SPF daily, even in winter",
                    "Deep condition your hair weekly",
                    "Exfoliate 2-3 times per week for glowing skin",
                    "Schedule regular trims to keep hair healthy"
                ],
                'value_props': [
                    "enhancing your natural beauty",
                    "providing relaxing spa experiences",
                    "using high-quality, safe products",
                    "helping you feel confident and beautiful",
                    "creating personalized beauty solutions"
                ],
                'hashtags': ['#beauty', '#spa', '#skincare', '#salon', '#selfcare', '#beautytips', '#glowup']
            },
            'food': {
                'offers': [
                    "Happy hour: 50% off appetizers 3-6pm",
                    "Weekend brunch special: $15 bottomless mimosas",
                    "Family dinner deal: Kids eat free Sundays",
                    "Date night package: Dinner for two $49",
                    "Catering 20% off for orders over $200"
                ],
                'tips': [
                    "Try new flavors - expand your palate",
                    "Fresh, local ingredients make all the difference",
                    "Pair wines with complementary dishes",
                    "Save room for dessert - life's too short",
                    "Share dishes to try more variety"
                ],
                'value_props': [
                    "serving fresh, locally-sourced ingredients",
                    "creating memorable dining experiences",
                    "bringing people together over great food",
                    "supporting local farmers and suppliers",
                    "crafting dishes with passion and care"
                ],
                'hashtags': ['#restaurant', '#food', '#dining', '#localfood', '#freshingredients', '#foodie', '#delicious']
            },
            'general': {
                'offers': [
                    "New customer discount: 20% off first service",
                    "Loyalty rewards program now available",
                    "Refer a friend and save",
                    "Seasonal promotion: Limited time only",
                    "Bundle deals available"
                ],
                'tips': [
                    "Quality service makes all the difference",
                    "Building relationships is key to business success",
                    "Customer satisfaction is our top priority",
                    "Continuous improvement drives excellence",
                    "Local businesses strengthen communities"
                ],
                'value_props': [
                    "providing exceptional customer service",
                    "delivering quality results every time",
                    "supporting our local community",
                    "building lasting relationships",
                    "exceeding customer expectations"
                ],
                'hashtags': ['#business', '#service', '#quality', '#community', '#local', '#customerservice']
            }
        }
        
        # Call to action options
        self.cta_options = [
            "Book now!",
            "Call to schedule your appointment.",
            "Visit us today!",
            "DM us for more info.",
            "Link in bio to book online.",
            "Stop by or give us a call!",
            "Schedule online or call us.",
            "Don't wait - spaces are limited!",
            "Contact us to learn more.",
            "Book your spot today!"
        ]
        
        # Days of the week for scheduling
        self.days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    def generate_posts(self, business_profile: Dict, post_preferences: Dict, industry_news: List[Dict] = None) -> List[Dict]:
        """
        Generate Facebook posts based on business profile and preferences
        
        Args:
            business_profile: Business information and characteristics
            post_preferences: Tone, type, frequency preferences
            industry_news: Optional industry news for insight posts
            
        Returns:
            List of generated post objects
        """
        posts = []
        
        # Extract preferences
        tone = post_preferences.get('tone', 'professional')
        frequency = post_preferences.get('frequency', 3)
        preferred_types = post_preferences.get('post_types', ['promo', 'tip', 'update', 'insight'])
        
        # Generate mix of post types
        post_types = self._distribute_post_types(frequency, preferred_types)
        
        for post_type in post_types:
            if post_type == 'insight' and industry_news:
                post = self._generate_insight_post(business_profile, tone, industry_news)
            else:
                post = self._generate_standard_post(business_profile, tone, post_type)
            
            if post:
                posts.append(post)
        
        return posts
    
    def _distribute_post_types(self, frequency: int, preferred_types: List[str]) -> List[str]:
        """Distribute post types across the requested frequency"""
        if not preferred_types:
            preferred_types = ['promo', 'tip', 'update']
        
        post_types = []
        
        # Ensure variety in post types
        for i in range(frequency):
            post_type = preferred_types[i % len(preferred_types)]
            post_types.append(post_type)
        
        return post_types
    
    def _generate_standard_post(self, business_profile: Dict, tone: str, post_type: str) -> Dict:
        """Generate a standard post (promo, tip, update)"""
        industry = business_profile.get('industry', 'general')
        business_name = business_profile.get('business_name', 'Our Business')
        
        # Get industry-specific content
        industry_data = self.industry_content.get(industry, self.industry_content['general'])
        
        # Get template
        templates = self.post_templates[post_type][tone]
        template = random.choice(templates)
        
        # Prepare content variables
        content_vars = {
            'business_name': business_name,
            'call_to_action': random.choice(self.cta_options),
            'value_prop': random.choice(industry_data['value_props'])
        }
        
        # Type-specific content
        if post_type == 'promo':
            content_vars['offer'] = random.choice(industry_data['offers'])
        elif post_type == 'tip':
            content_vars['tip_content'] = random.choice(industry_data['tips'])
            content_vars['benefit'] = random.choice(['succeed', 'improve', 'feel great', 'achieve your goals'])
        elif post_type == 'update':
            updates = [
                "We've extended our hours for your convenience",
                "New services now available",
                "We're implementing new safety protocols",
                "Our team has completed additional training",
                "We've upgraded our facilities"
            ]
            content_vars['update_content'] = random.choice(updates)
        
        # Add contact info if available
        contact_info = business_profile.get('contact_info', {})
        if contact_info.get('phone'):
            content_vars['contact_info'] = f"📞 {contact_info['phone']}"
        else:
            content_vars['contact_info'] = ""
        
        # Format the post
        try:
            content = template.format(**content_vars)
        except KeyError:
            # Fallback if template formatting fails
            content = f"Great news from {business_name}! {content_vars.get('offer', 'We have something special for you.')} {content_vars['call_to_action']}"
        
        # Generate hashtags
        hashtags = self._generate_hashtags(industry_data['hashtags'], post_type)
        
        post = {
            'content': content,
            'hashtags': hashtags,
            'post_type': post_type,
            'tone': tone,
            'industry': industry,
            'call_to_action': content_vars['call_to_action'],
            'estimated_engagement': self._estimate_engagement(post_type, tone),
            'best_time_to_post': self._suggest_best_time(industry, post_type)
        }
        
        return post
    
    def _generate_insight_post(self, business_profile: Dict, tone: str, industry_news: List[Dict]) -> Dict:
        """Generate an insight post based on industry news"""
        if not industry_news:
            return self._generate_standard_post(business_profile, tone, 'tip')
        
        industry = business_profile.get('industry', 'general')
        business_name = business_profile.get('business_name', 'Our Business')
        
        # Select a news item
        news_item = random.choice(industry_news)
        
        # Get template
        templates = self.post_templates['insight'][tone]
        template = random.choice(templates)
        
        # Use business insights from news item
        insight_content = news_item.get('headline', 'Industry trends continue to evolve')
        
        # Format the post
        content_vars = {
            'business_name': business_name,
            'insight_content': insight_content,
            'call_to_action': random.choice(self.cta_options)
        }
        
        try:
            content = template.format(**content_vars)
        except KeyError:
            content = f"Industry update: {insight_content} Stay informed with {business_name}! {content_vars['call_to_action']}"
        
        # Generate hashtags
        industry_data = self.industry_content.get(industry, self.industry_content['general'])
        hashtags = self._generate_hashtags(industry_data['hashtags'] + ['#industrytrends', '#businessinsights'], 'insight')
        
        post = {
            'content': content,
            'hashtags': hashtags,
            'post_type': 'insight',
            'tone': tone,
            'industry': industry,
            'call_to_action': content_vars['call_to_action'],
            'news_source': news_item.get('source', 'Industry Reports'),
            'estimated_engagement': self._estimate_engagement('insight', tone),
            'best_time_to_post': self._suggest_best_time(industry, 'insight')
        }
        
        return post
    
    def _generate_hashtags(self, base_hashtags: List[str], post_type: str) -> List[str]:
        """Generate relevant hashtags for the post"""
        hashtags = base_hashtags.copy()
        
        # Add post-type specific hashtags
        type_hashtags = {
            'promo': ['#deal', '#offer', '#special', '#save'],
            'tip': ['#tips', '#advice', '#howto', '#expert'],
            'update': ['#news', '#update', '#announcement'],
            'insight': ['#trends', '#insights', '#industry', '#knowledge']
        }
        
        hashtags.extend(type_hashtags.get(post_type, []))
        
        # Add general business hashtags
        hashtags.extend(['#local', '#smallbusiness', '#community'])
        
        # Limit and randomize
        return random.sample(hashtags, min(8, len(hashtags)))
    
    def _estimate_engagement(self, post_type: str, tone: str) -> Dict:
        """Estimate engagement potential for the post"""
        base_scores = {
            'promo': {'likes': 45, 'comments': 8, 'shares': 12},
            'tip': {'likes': 65, 'comments': 15, 'shares': 25},
            'update': {'likes': 35, 'comments': 6, 'shares': 8},
            'insight': {'likes': 55, 'comments': 12, 'shares': 20}
        }
        
        tone_multipliers = {
            'friendly': 1.2,
            'casual': 1.1,
            'professional': 1.0,
            'premium': 0.9
        }
        
        base = base_scores.get(post_type, {'likes': 50, 'comments': 10, 'shares': 15})
        multiplier = tone_multipliers.get(tone, 1.0)
        
        return {
            'estimated_likes': int(base['likes'] * multiplier),
            'estimated_comments': int(base['comments'] * multiplier),
            'estimated_shares': int(base['shares'] * multiplier),
            'engagement_score': 'high' if multiplier > 1.1 else 'medium'
        }
    
    def _suggest_best_time(self, industry: str, post_type: str) -> str:
        """Suggest best time to post based on industry and type"""
        industry_times = {
            'fitness': {'morning': '6:00 AM', 'evening': '6:00 PM'},
            'beauty': {'afternoon': '2:00 PM', 'evening': '7:00 PM'},
            'food': {'lunch': '11:30 AM', 'dinner': '5:30 PM'},
            'general': {'morning': '9:00 AM', 'afternoon': '3:00 PM'}
        }
        
        post_type_times = {
            'promo': 'afternoon',
            'tip': 'morning',
            'update': 'morning',
            'insight': 'afternoon'
        }
        
        industry_schedule = industry_times.get(industry, industry_times['general'])
        preferred_slot = post_type_times.get(post_type, 'afternoon')
        
        return industry_schedule.get(preferred_slot, '12:00 PM')
    
    def create_weekly_schedule(self, posts: List[Dict], frequency: int, 
                             preferred_days: List[str] = None, start_date: str = None) -> Dict:
        """
        Create a weekly posting schedule
        
        Args:
            posts: List of posts to schedule
            frequency: Number of posts per week
            preferred_days: Preferred days to post
            start_date: Week start date (YYYY-MM-DD)
            
        Returns:
            Weekly schedule with posts mapped to days
        """
        if start_date:
            start = datetime.strptime(start_date, '%Y-%m-%d')
        else:
            start = datetime.now()
        
        # Default posting days if none specified
        if not preferred_days:
            if frequency <= 3:
                preferred_days = ['monday', 'wednesday', 'friday']
            elif frequency <= 5:
                preferred_days = ['monday', 'tuesday', 'thursday', 'friday', 'saturday']
            else:
                preferred_days = self.days
        
        # Ensure we have enough days
        posting_days = preferred_days[:frequency]
        if len(posting_days) < frequency:
            remaining_days = [day for day in self.days if day not in posting_days]
            posting_days.extend(remaining_days[:frequency - len(posting_days)])
        
        # Create schedule
        schedule = {}
        
        for i, day in enumerate(self.days):
            day_date = start + timedelta(days=i)
            
            if day in posting_days and posting_days.index(day) < len(posts):
                post_index = posting_days.index(day)
                post = posts[post_index]
                
                schedule[day] = {
                    'date': day_date.strftime('%Y-%m-%d'),
                    'post': post,
                    'suggested_time': post.get('best_time_to_post', '12:00 PM'),
                    'day_of_week': day.title()
                }
            else:
                schedule[day] = {
                    'date': day_date.strftime('%Y-%m-%d'),
                    'post': None,
                    'suggested_time': None,
                    'day_of_week': day.title()
                }
        
        return schedule

# Test function
def test_content_generator():
    """Test the content generator"""
    generator = ContentGenerator()
    
    # Mock business profile
    business_profile = {
        'business_name': 'FitZone Gym',
        'industry': 'fitness',
        'description': 'A modern fitness center focused on personal training',
        'tone_of_voice': 'friendly',
        'contact_info': {'phone': '555-0123'}
    }
    
    # Mock preferences
    preferences = {
        'tone': 'friendly',
        'frequency': 3,
        'post_types': ['promo', 'tip', 'insight']
    }
    
    # Mock industry news
    industry_news = [{
        'headline': 'HIIT workouts gain popularity among busy professionals',
        'source': 'Fitness Magazine'
    }]
    
    # Generate posts
    posts = generator.generate_posts(business_profile, preferences, industry_news)
    
    print("Generated Posts:")
    for i, post in enumerate(posts, 1):
        print(f"\n--- Post {i} ---")
        print(f"Type: {post['post_type']}")
        print(f"Content: {post['content']}")
        print(f"Hashtags: {' '.join(post['hashtags'])}")
        print(f"Best time: {post['best_time_to_post']}")
    
    # Test weekly schedule
    schedule = generator.create_weekly_schedule(posts, 3, ['monday', 'wednesday', 'friday'])
    
    print("\n\nWeekly Schedule:")
    for day, info in schedule.items():
        if info['post']:
            print(f"{info['day_of_week']}: {info['post']['post_type']} post at {info['suggested_time']}")

if __name__ == "__main__":
    test_content_generator()