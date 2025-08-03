# app.py - Main Flask Application
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import uuid

# Import our modules
from business_analyzer import BusinessAnalyzer
from news_analyzer import NewsAnalyzer
from content_generator import ContentGenerator
from facebook_integration import FacebookIntegration
from data_storage import DataStorage

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
business_analyzer = BusinessAnalyzer()
news_analyzer = NewsAnalyzer()
content_generator = ContentGenerator()
facebook_integration = FacebookIntegration()
data_storage = DataStorage()

# =====================================
# 1. Business Understanding API
# =====================================

@app.route('/api/business/analyze', methods=['POST'])
def analyze_business():
    """
    Analyze a business website and extract structured profile
    Input: {"website_url": "https://example.com"}
    Output: Business profile with name, industry, services, tone
    """
    try:
        data = request.get_json()
        if not data or 'website_url' not in data:
            return jsonify({'error': 'website_url is required'}), 400
        
        website_url = data['website_url']
        business_profile = business_analyzer.analyze_website(website_url)
        
        # Store the business profile
        business_id = str(uuid.uuid4())
        data_storage.store_business_profile(business_id, business_profile)
        
        return jsonify({
            'success': True,
            'business_id': business_id,
            'profile': business_profile
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/business/<business_id>', methods=['GET'])
def get_business_profile(business_id):
    """Get stored business profile"""
    try:
        profile = data_storage.get_business_profile(business_id)
        if not profile:
            return jsonify({'error': 'Business profile not found'}), 404
        
        return jsonify({
            'success': True,
            'profile': profile
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 2. Industry News Analyzer API
# =====================================

@app.route('/api/news/analyze', methods=['POST'])
def analyze_industry_news():
    """
    Get current industry news and insights
    Input: {"industry": "fitness", "keywords": ["gym", "workout"]}
    Output: List of 3-5 current headlines and insights
    """
    try:
        data = request.get_json()
        if not data or 'industry' not in data:
            return jsonify({'error': 'industry is required'}), 400
        
        industry = data['industry']
        keywords = data.get('keywords', [])
        
        news_insights = news_analyzer.get_industry_news(industry, keywords)
        
        return jsonify({
            'success': True,
            'industry': industry,
            'insights': news_insights
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 3. Content Generator API
# =====================================

@app.route('/api/content/generate', methods=['POST'])
def generate_content():
    """
    Generate Facebook post content based on business profile and industry news
    Input: {
        "business_id": "uuid",
        "post_preferences": {
            "tone": "professional|witty|friendly",
            "post_type": "promo|tip|update|insight",
            "frequency": 3
        },
        "industry_news": [...] (optional)
    }
    Output: List of ready-to-publish post captions
    """
    try:
        data = request.get_json()
        if not data or 'business_id' not in data:
            return jsonify({'error': 'business_id is required'}), 400
        
        business_id = data['business_id']
        business_profile = data_storage.get_business_profile(business_id)
        
        if not business_profile:
            return jsonify({'error': 'Business profile not found'}), 404
        
        post_preferences = data.get('post_preferences', {})
        industry_news = data.get('industry_news', [])
        
        # Generate content
        generated_posts = content_generator.generate_posts(
            business_profile=business_profile,
            post_preferences=post_preferences,
            industry_news=industry_news
        )
        
        # Store generated posts
        for post in generated_posts:
            post['id'] = str(uuid.uuid4())
            post['business_id'] = business_id
            post['created_at'] = datetime.now().isoformat()
            post['status'] = 'draft'
            data_storage.store_post(post['id'], post)
        
        return jsonify({
            'success': True,
            'posts': generated_posts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 4. Weekly Planner API
# =====================================

@app.route('/api/planner/schedule', methods=['POST'])
def create_weekly_schedule():
    """
    Create a weekly posting schedule
    Input: {
        "business_id": "uuid",
        "frequency": 3,
        "preferred_days": ["monday", "wednesday", "friday"],
        "start_date": "2025-08-04"
    }
    Output: Weekly schedule with posts mapped to specific days
    """
    try:
        data = request.get_json()
        if not data or 'business_id' not in data:
            return jsonify({'error': 'business_id is required'}), 400
        
        business_id = data['business_id']
        frequency = data.get('frequency', 3)
        preferred_days = data.get('preferred_days', [])
        start_date = data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Get available posts for this business
        available_posts = data_storage.get_posts_by_business(business_id)
        draft_posts = [p for p in available_posts if p.get('status') == 'draft']
        
        if len(draft_posts) < frequency:
            return jsonify({'error': f'Not enough posts available. Need {frequency}, have {len(draft_posts)}'}), 400
        
        # Create weekly schedule
        schedule = content_generator.create_weekly_schedule(
            posts=draft_posts[:frequency],
            frequency=frequency,
            preferred_days=preferred_days,
            start_date=start_date
        )
        
        # Update post statuses to scheduled
        schedule_id = str(uuid.uuid4())
        for day, post_info in schedule.items():
            if post_info and post_info.get('post'):
                post_id = post_info['post']['id']
                post_info['post']['status'] = 'scheduled'
                post_info['post']['scheduled_date'] = post_info['date']
                data_storage.update_post(post_id, post_info['post'])
        
        data_storage.store_schedule(schedule_id, {
            'business_id': business_id,
            'schedule': schedule,
            'created_at': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'schedule_id': schedule_id,
            'schedule': schedule
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/planner/schedule/<schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    """Get a specific schedule"""
    try:
        schedule = data_storage.get_schedule(schedule_id)
        if not schedule:
            return jsonify({'error': 'Schedule not found'}), 404
        
        return jsonify({
            'success': True,
            'schedule': schedule
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 5. Preview & Edit API
# =====================================

@app.route('/api/posts/scheduled/<business_id>', methods=['GET'])
def get_scheduled_posts(business_id):
    """Get all scheduled posts for a business"""
    try:
        posts = data_storage.get_posts_by_business(business_id)
        scheduled_posts = [p for p in posts if p.get('status') == 'scheduled']
        
        return jsonify({
            'success': True,
            'posts': scheduled_posts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Update post content before publishing"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        existing_post = data_storage.get_post(post_id)
        if not existing_post:
            return jsonify({'error': 'Post not found'}), 404
        
        # Update allowed fields
        updatable_fields = ['content', 'hashtags', 'call_to_action', 'scheduled_date']
        for field in updatable_fields:
            if field in data:
                existing_post[field] = data[field]
        
        existing_post['updated_at'] = datetime.now().isoformat()
        data_storage.update_post(post_id, existing_post)
        
        return jsonify({
            'success': True,
            'post': existing_post
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a scheduled post"""
    try:
        success = data_storage.delete_post(post_id)
        if not success:
            return jsonify({'error': 'Post not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Post deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 6. Facebook Page Connection
# =====================================

@app.route('/api/facebook/connect', methods=['POST'])
def connect_facebook_page():
    """
    Connect to Facebook page (initially mock, then real)
    Input: {"access_token": "...", "page_id": "..."}
    Output: Connection status and page info
    """
    try:
        data = request.get_json()
        if not data or 'access_token' not in data:
            return jsonify({'error': 'access_token is required'}), 400
        
        access_token = data['access_token']
        page_id = data.get('page_id')
        
        # Connect to Facebook
        connection_result = facebook_integration.connect_page(access_token, page_id)
        
        return jsonify({
            'success': True,
            'connection': connection_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/facebook/pages', methods=['GET'])
def get_facebook_pages():
    """Get available Facebook pages for connected account"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization header required'}), 401
        
        access_token = auth_header.replace('Bearer ', '')
        pages = facebook_integration.get_user_pages(access_token)
        
        return jsonify({
            'success': True,
            'pages': pages
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# 7. Post Publishing
# =====================================

@app.route('/api/posts/<post_id>/publish', methods=['POST'])
def publish_post(post_id):
    """
    Publish a post to Facebook
    Input: {"page_id": "...", "access_token": "..."}
    Output: Published post info with FB post link
    """
    try:
        data = request.get_json()
        post = data_storage.get_post(post_id)
        
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        
        page_id = data.get('page_id')
        access_token = data.get('access_token')
        
        if not page_id or not access_token:
            return jsonify({'error': 'page_id and access_token are required'}), 400
        
        # Publish to Facebook
        publish_result = facebook_integration.publish_post(
            access_token=access_token,
            page_id=page_id,
            content=post['content'],
            post_data=post
        )
        
        # Update post status
        post['status'] = 'published'
        post['published_at'] = datetime.now().isoformat()
        post['facebook_post_id'] = publish_result.get('post_id')
        post['facebook_url'] = publish_result.get('post_url')
        data_storage.update_post(post_id, post)
        
        return jsonify({
            'success': True,
            'post': post,
            'facebook_result': publish_result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =====================================
# Health Check and Utility Endpoints
# =====================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'AI Social Media Manager Backend is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/business/<business_id>/posts', methods=['GET'])
def get_business_posts(business_id):
    """Get all posts for a business"""
    try:
        posts = data_storage.get_posts_by_business(business_id)
        return jsonify({
            'success': True,
            'posts': posts
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)