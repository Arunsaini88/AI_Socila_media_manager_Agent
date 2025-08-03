# facebook_integration.py
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class FacebookIntegration:
    """Handles Facebook Graph API integration for page management and posting"""
    
    def __init__(self):
        self.graph_api_base = "https://graph.facebook.com/v18.0"
        self.session = requests.Session()
        
        # Mock mode for testing without real Facebook API
        self.mock_mode = True  # Set to False for real Facebook integration
        
        # Mock data for testing
        self.mock_pages = [
            {
                'id': '123456789',
                'name': 'Test Business Page',
                'access_token': 'mock_page_token_123',
                'category': 'Local Business',
                'fan_count': 245
            },
            {
                'id': '987654321', 
                'name': 'Demo Restaurant',
                'access_token': 'mock_page_token_456',
                'category': 'Restaurant',
                'fan_count': 156
            }
        ]
        
        self.mock_posts = {}  # Store mock published posts
    
    def connect_page(self, access_token: str, page_id: str = None) -> Dict:
        """
        Connect to Facebook page and verify access
        
        Args:
            access_token: Facebook user access token
            page_id: Optional specific page ID to connect to
            
        Returns:
            Connection result with page information
        """
        if self.mock_mode:
            return self._mock_connect_page(access_token, page_id)
        
        try:
            # Get user's pages
            pages = self.get_user_pages(access_token)
            
            if not pages:
                return {
                    'success': False,
                    'error': 'No pages found for this account'
                }
            
            # If specific page requested, find it
            if page_id:
                selected_page = next((page for page in pages if page['id'] == page_id), None)
                if not selected_page:
                    return {
                        'success': False,
                        'error': f'Page {page_id} not found or no access'
                    }
            else:
                # Use first page by default
                selected_page = pages[0]
            
            # Verify page permissions
            permissions = self._check_page_permissions(selected_page['access_token'], selected_page['id'])
            
            return {
                'success': True,
                'page': selected_page,
                'permissions': permissions,
                'connected_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_connect_page(self, access_token: str, page_id: str = None) -> Dict:
        """Mock page connection for testing"""
        if page_id:
            page = next((p for p in self.mock_pages if p['id'] == page_id), None)
            if not page:
                return {
                    'success': False,
                    'error': f'Page {page_id} not found'
                }
        else:
            page = self.mock_pages[0]
        
        return {
            'success': True,
            'page': page,
            'permissions': ['manage_pages', 'publish_pages', 'pages_show_list'],
            'connected_at': datetime.now().isoformat(),
            'mock_mode': True
        }
    
    def get_user_pages(self, access_token: str) -> List[Dict]:
        """
        Get list of pages user can manage
        
        Args:
            access_token: Facebook user access token
            
        Returns:
            List of page information
        """
        if self.mock_mode:
            return self.mock_pages
        
        try:
            url = f"{self.graph_api_base}/me/accounts"
            params = {
                'access_token': access_token,
                'fields': 'id,name,access_token,category,fan_count,picture'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            pages = data.get('data', [])
            
            return pages
            
        except Exception as e:
            print(f"Error fetching pages: {e}")
            return []
    
    def _check_page_permissions(self, page_access_token: str, page_id: str) -> List[str]:
        """Check what permissions we have for the page"""
        if self.mock_mode:
            return ['manage_pages', 'publish_pages', 'pages_show_list']
        
        try:
            url = f"{self.graph_api_base}/{page_id}"
            params = {
                'access_token': page_access_token,
                'fields': 'permissions'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('permissions', [])
            
        except Exception as e:
            print(f"Error checking permissions: {e}")
            return []
    
    def publish_post(self, access_token: str, page_id: str, content: str, 
                    post_data: Dict = None, scheduled_time: str = None) -> Dict:
        """
        Publish a post to Facebook page
        
        Args:
            access_token: Page access token
            page_id: Facebook page ID
            content: Post content text
            post_data: Additional post data (hashtags, etc.)
            scheduled_time: Optional scheduled publish time (ISO format)
            
        Returns:
            Publication result with post ID and URL
        """
        if self.mock_mode:
            return self._mock_publish_post(access_token, page_id, content, post_data, scheduled_time)
        
        try:
            url = f"{self.graph_api_base}/{page_id}/feed"
            
            # Prepare post content
            message = content
            if post_data and post_data.get('hashtags'):
                hashtags = ' '.join(post_data['hashtags'])
                message = f"{content}\n\n{hashtags}"
            
            post_params = {
                'access_token': access_token,
                'message': message
            }
            
            # Add scheduled publishing if specified
            if scheduled_time:
                try:
                    scheduled_dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
                    scheduled_timestamp = int(scheduled_dt.timestamp())
                    post_params['scheduled_publish_time'] = scheduled_timestamp
                    post_params['published'] = False
                except Exception as e:
                    print(f"Error parsing scheduled time: {e}")
            
            # Add link if present in post data
            if post_data and post_data.get('link'):
                post_params['link'] = post_data['link']
            
            response = self.session.post(url, data=post_params)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('id')
            
            # Generate post URL
            post_url = f"https://facebook.com/{page_id}/posts/{post_id.split('_')[1]}" if post_id else None
            
            return {
                'success': True,
                'post_id': post_id,
                'post_url': post_url,
                'published_at': datetime.now().isoformat(),
                'scheduled': bool(scheduled_time)
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Facebook API error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_publish_post(self, access_token: str, page_id: str, content: str, 
                          post_data: Dict = None, scheduled_time: str = None) -> Dict:
        """Mock post publishing for testing"""
        
        # Generate mock post ID
        post_id = f"{page_id}_{uuid.uuid4().hex[:10]}"
        
        # Store mock post
        self.mock_posts[post_id] = {
            'id': post_id,
            'page_id': page_id,
            'content': content,
            'post_data': post_data,
            'published_at': datetime.now().isoformat(),
            'scheduled_time': scheduled_time,
            'is_scheduled': bool(scheduled_time)
        }
        
        # Generate mock post URL
        post_url = f"https://facebook.com/mock-page/{post_id}"
        
        return {
            'success': True,
            'post_id': post_id,
            'post_url': post_url,
            'published_at': datetime.now().isoformat(),
            'scheduled': bool(scheduled_time),
            'mock_mode': True
        }
    
    def get_page_insights(self, access_token: str, page_id: str, 
                         metric: str = 'page_impressions', period: str = 'day') -> Dict:
        """
        Get page insights/analytics
        
        Args:
            access_token: Page access token
            page_id: Facebook page ID
            metric: Metric to retrieve
            period: Time period (day, week, days_28)
            
        Returns:
            Insights data
        """
        if self.mock_mode:
            return self._mock_page_insights(page_id, metric, period)
        
        try:
            url = f"{self.graph_api_base}/{page_id}/insights"
            params = {
                'access_token': access_token,
                'metric': metric,
                'period': period
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_page_insights(self, page_id: str, metric: str, period: str) -> Dict:
        """Mock page insights for testing"""
        import random
        
        # Generate mock data based on metric
        if metric == 'page_impressions':
            value = random.randint(1000, 5000)
        elif metric == 'page_reach':
            value = random.randint(500, 2000)
        elif metric == 'page_engaged_users':
            value = random.randint(50, 500)
        else:
            value = random.randint(10, 1000)
        
        return {
            'data': [{
                'name': metric,
                'period': period,
                'values': [{
                    'value': value,
                    'end_time': datetime.now().isoformat()
                }]
            }],
            'mock_mode': True
        }
    
    def get_post_insights(self, access_token: str, post_id: str) -> Dict:
        """
        Get insights for a specific post
        
        Args:
            access_token: Page access token
            post_id: Facebook post ID
            
        Returns:
            Post insights data
        """
        if self.mock_mode:
            return self._mock_post_insights(post_id)
        
        try:
            url = f"{self.graph_api_base}/{post_id}/insights"
            params = {
                'access_token': access_token,
                'metric': 'post_impressions,post_reach,post_engaged_users'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_post_insights(self, post_id: str) -> Dict:
        """Mock post insights for testing"""
        import random
        
        return {
            'data': [
                {
                    'name': 'post_impressions',
                    'values': [{'value': random.randint(100, 1000)}]
                },
                {
                    'name': 'post_reach',
                    'values': [{'value': random.randint(50, 500)}]
                },
                {
                    'name': 'post_engaged_users',
                    'values': [{'value': random.randint(10, 100)}]
                }
            ],
            'mock_mode': True
        }
    
    def delete_post(self, access_token: str, post_id: str) -> Dict:
        """
        Delete a Facebook post
        
        Args:
            access_token: Page access token
            post_id: Facebook post ID
            
        Returns:
            Deletion result
        """
        if self.mock_mode:
            return self._mock_delete_post(post_id)
        
        try:
            url = f"{self.graph_api_base}/{post_id}"
            params = {
                'access_token': access_token
            }
            
            response = self.session.delete(url, params=params)
            response.raise_for_status()
            
            return {
                'success': True,
                'deleted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _mock_delete_post(self, post_id: str) -> Dict:
        """Mock post deletion for testing"""
        if post_id in self.mock_posts:
            del self.mock_posts[post_id]
            return {
                'success': True,
                'deleted_at': datetime.now().isoformat(),
                'mock_mode': True
            }
        else:
            return {
                'success': False,
                'error': 'Post not found',
                'mock_mode': True
            }
    
    def schedule_post(self, access_token: str, page_id: str, content: str, 
                     scheduled_time: str, post_data: Dict = None) -> Dict:
        """
        Schedule a post for future publishing
        
        Args:
            access_token: Page access token
            page_id: Facebook page ID
            content: Post content
            scheduled_time: When to publish (ISO format)
            post_data: Additional post data
            
        Returns:
            Scheduling result
        """
        return self.publish_post(
            access_token=access_token,
            page_id=page_id,
            content=content,
            post_data=post_data,
            scheduled_time=scheduled_time
        )
    
    def get_scheduled_posts(self, access_token: str, page_id: str) -> List[Dict]:
        """
        Get scheduled posts for a page
        
        Args:
            access_token: Page access token
            page_id: Facebook page ID
            
        Returns:
            List of scheduled posts
        """
        if self.mock_mode:
            return self._mock_scheduled_posts(page_id)
        
        try:
            url = f"{self.graph_api_base}/{page_id}/scheduled_posts"
            params = {
                'access_token': access_token,
                'fields': 'id,message,scheduled_publish_time,created_time'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get('data', [])
            
        except Exception as e:
            print(f"Error fetching scheduled posts: {e}")
            return []
    
    def _mock_scheduled_posts(self, page_id: str) -> List[Dict]:
        """Mock scheduled posts for testing"""
        scheduled_posts = []
        
        for post_id, post_data in self.mock_posts.items():
            if post_data.get('page_id') == page_id and post_data.get('scheduled_time'):
                scheduled_posts.append({
                    'id': post_id,
                    'message': post_data['content'],
                    'scheduled_publish_time': post_data['scheduled_time'],
                    'created_time': post_data['published_at']
                })
        
        return scheduled_posts
    
    def enable_real_mode(self):
        """Enable real Facebook API mode"""
        self.mock_mode = False
        print("Facebook integration switched to REAL mode - will use actual Facebook API")
    
    def enable_mock_mode(self):
        """Enable mock mode for testing"""
        self.mock_mode = True
        print("Facebook integration switched to MOCK mode - safe for testing")

# Test function
def test_facebook_integration():
    """Test the Facebook integration"""
    fb = FacebookIntegration()
    
    # Test connection
    print("Testing Facebook connection...")
    connection = fb.connect_page('mock_user_token')
    print(f"Connection result: {connection}")
    
    if connection['success']:
        page = connection['page']
        
        # Test post publishing
        print("\nTesting post publishing...")
        post_result = fb.publish_post(
            access_token=page['access_token'],
            page_id=page['id'],
            content="Test post from our AI social media manager! 🚀",
            post_data={
                'hashtags': ['#test', '#AI', '#socialmedia'],
                'post_type': 'promo'
            }
        )
        print(f"Post result: {post_result}")
        
        # Test insights
        if post_result['success']:
            print("\nTesting post insights...")
            insights = fb.get_post_insights(page['access_token'], post_result['post_id'])
            print(f"Insights: {insights}")
    
    # Test page listing
    print("\nTesting page listing...")
    pages = fb.get_user_pages('mock_user_token')
    print(f"Available pages: {len(pages)} found")
    for page in pages:
        print(f"- {page['name']} (ID: {page['id']})")

if __name__ == "__main__":
    test_facebook_integration()