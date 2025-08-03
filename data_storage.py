# data_storage.py
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class DataStorage:
    """Handles data persistence for business profiles, posts, schedules, and other data"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.ensure_data_directory()
        
        # File paths for different data types
        self.business_profiles_file = os.path.join(data_dir, 'business_profiles.json')
        self.posts_file = os.path.join(data_dir, 'posts.json')
        self.schedules_file = os.path.join(data_dir, 'schedules.json')
        self.facebook_connections_file = os.path.join(data_dir, 'facebook_connections.json')
        
        # Initialize data files if they don't exist
        self.initialize_data_files()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def initialize_data_files(self):
        """Initialize JSON data files with empty structures"""
        files_to_init = [
            self.business_profiles_file,
            self.posts_file,
            self.schedules_file,
            self.facebook_connections_file
        ]
        
        for file_path in files_to_init:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f, indent=2)
    
    # =====================================
    # Business Profile Operations
    # =====================================
    
    def store_business_profile(self, business_id: str, profile: Dict) -> bool:
        """Store a business profile"""
        try:
            profiles = self._load_json_file(self.business_profiles_file)
            
            profile['id'] = business_id
            profile['created_at'] = datetime.now().isoformat()
            profile['updated_at'] = datetime.now().isoformat()
            
            profiles[business_id] = profile
            
            return self._save_json_file(self.business_profiles_file, profiles)
            
        except Exception as e:
            print(f"Error storing business profile: {e}")
            return False
    
    def get_business_profile(self, business_id: str) -> Optional[Dict]:
        """Retrieve a business profile"""
        try:
            profiles = self._load_json_file(self.business_profiles_file)
            return profiles.get(business_id)
            
        except Exception as e:
            print(f"Error retrieving business profile: {e}")
            return None
    
    def update_business_profile(self, business_id: str, updates: Dict) -> bool:
        """Update a business profile"""
        try:
            profiles = self._load_json_file(self.business_profiles_file)
            
            if business_id not in profiles:
                return False
            
            profiles[business_id].update(updates)
            profiles[business_id]['updated_at'] = datetime.now().isoformat()
            
            return self._save_json_file(self.business_profiles_file, profiles)
            
        except Exception as e:
            print(f"Error updating business profile: {e}")
            return False
    
    def list_business_profiles(self) -> List[Dict]:
        """List all business profiles"""
        try:
            profiles = self._load_json_file(self.business_profiles_file)
            return list(profiles.values())
            
        except Exception as e:
            print(f"Error listing business profiles: {e}")
            return []
    
    def delete_business_profile(self, business_id: str) -> bool:
        """Delete a business profile"""
        try:
            profiles = self._load_json_file(self.business_profiles_file)
            
            if business_id in profiles:
                del profiles[business_id]
                return self._save_json_file(self.business_profiles_file, profiles)
            
            return False
            
        except Exception as e:
            print(f"Error deleting business profile: {e}")
            return False
    
    # =====================================
    # Post Operations
    # =====================================
    
    def store_post(self, post_id: str, post: Dict) -> bool:
        """Store a post"""
        try:
            posts = self._load_json_file(self.posts_file)
            
            post['id'] = post_id
            post['created_at'] = datetime.now().isoformat()
            post['updated_at'] = datetime.now().isoformat()
            
            posts[post_id] = post
            
            return self._save_json_file(self.posts_file, posts)
            
        except Exception as e:
            print(f"Error storing post: {e}")
            return False
    
    def get_post(self, post_id: str) -> Optional[Dict]:
        """Retrieve a post"""
        try:
            posts = self._load_json_file(self.posts_file)
            return posts.get(post_id)
            
        except Exception as e:
            print(f"Error retrieving post: {e}")
            return None
    
    def update_post(self, post_id: str, updates: Dict) -> bool:
        """Update a post"""
        try:
            posts = self._load_json_file(self.posts_file)
            
            if post_id not in posts:
                return False
            
            posts[post_id].update(updates)
            posts[post_id]['updated_at'] = datetime.now().isoformat()
            
            return self._save_json_file(self.posts_file, posts)
            
        except Exception as e:
            print(f"Error updating post: {e}")
            return False
    
    def delete_post(self, post_id: str) -> bool:
        """Delete a post"""
        try:
            posts = self._load_json_file(self.posts_file)
            
            if post_id in posts:
                del posts[post_id]
                return self._save_json_file(self.posts_file, posts)
            
            return False
            
        except Exception as e:
            print(f"Error deleting post: {e}")
            return False
    
    def get_posts_by_business(self, business_id: str) -> List[Dict]:
        """Get all posts for a specific business"""
        try:
            posts = self._load_json_file(self.posts_file)
            business_posts = []
            
            for post in posts.values():
                if post.get('business_id') == business_id:
                    business_posts.append(post)
            
            # Sort by creation date (newest first)
            business_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return business_posts
            
        except Exception as e:
            print(f"Error retrieving posts by business: {e}")
            return []
    
    def get_posts_by_status(self, status: str, business_id: str = None) -> List[Dict]:
        """Get posts by status (draft, scheduled, published)"""
        try:
            posts = self._load_json_file(self.posts_file)
            filtered_posts = []
            
            for post in posts.values():
                if post.get('status') == status:
                    if business_id is None or post.get('business_id') == business_id:
                        filtered_posts.append(post)
            
            # Sort by creation date (newest first)
            filtered_posts.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return filtered_posts
            
        except Exception as e:
            print(f"Error retrieving posts by status: {e}")
            return []
    
    def get_scheduled_posts_for_date(self, date: str, business_id: str = None) -> List[Dict]:
        """Get scheduled posts for a specific date"""
        try:
            posts = self._load_json_file(self.posts_file)
            scheduled_posts = []
            
            for post in posts.values():
                if (post.get('status') == 'scheduled' and 
                    post.get('scheduled_date', '').startswith(date)):
                    if business_id is None or post.get('business_id') == business_id:
                        scheduled_posts.append(post)
            
            return scheduled_posts
            
        except Exception as e:
            print(f"Error retrieving scheduled posts for date: {e}")
            return []
    
    # =====================================
    # Schedule Operations
    # =====================================
    
    def store_schedule(self, schedule_id: str, schedule: Dict) -> bool:
        """Store a weekly schedule"""
        try:
            schedules = self._load_json_file(self.schedules_file)
            
            schedule['id'] = schedule_id
            schedule['created_at'] = datetime.now().isoformat()
            schedule['updated_at'] = datetime.now().isoformat()
            
            schedules[schedule_id] = schedule
            
            return self._save_json_file(self.schedules_file, schedules)
            
        except Exception as e:
            print(f"Error storing schedule: {e}")
            return False
    
    def get_schedule(self, schedule_id: str) -> Optional[Dict]:
        """Retrieve a schedule"""
        try:
            schedules = self._load_json_file(self.schedules_file)
            return schedules.get(schedule_id)
            
        except Exception as e:
            print(f"Error retrieving schedule: {e}")
            return None
    
    def get_schedules_by_business(self, business_id: str) -> List[Dict]:
        """Get all schedules for a specific business"""
        try:
            schedules = self._load_json_file(self.schedules_file)
            business_schedules = []
            
            for schedule in schedules.values():
                if schedule.get('business_id') == business_id:
                    business_schedules.append(schedule)
            
            # Sort by creation date (newest first)
            business_schedules.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return business_schedules
            
        except Exception as e:
            print(f"Error retrieving schedules by business: {e}")
            return []
    
    def update_schedule(self, schedule_id: str, updates: Dict) -> bool:
        """Update a schedule"""
        try:
            schedules = self._load_json_file(self.schedules_file)
            
            if schedule_id not in schedules:
                return False
            
            schedules[schedule_id].update(updates)
            schedules[schedule_id]['updated_at'] = datetime.now().isoformat()
            
            return self._save_json_file(self.schedules_file, schedules)
            
        except Exception as e:
            print(f"Error updating schedule: {e}")
            return False
    
    def delete_schedule(self, schedule_id: str) -> bool:
        """Delete a schedule"""
        try:
            schedules = self._load_json_file(self.schedules_file)
            
            if schedule_id in schedules:
                del schedules[schedule_id]
                return self._save_json_file(self.schedules_file, schedules)
            
            return False
            
        except Exception as e:
            print(f"Error deleting schedule: {e}")
            return False
    
    # =====================================
    # Facebook Connection Operations
    # =====================================
    
    def store_facebook_connection(self, business_id: str, connection_data: Dict) -> bool:
        """Store Facebook connection information"""
        try:
            connections = self._load_json_file(self.facebook_connections_file)
            
            connection_data['business_id'] = business_id
            connection_data['connected_at'] = datetime.now().isoformat()
            connection_data['updated_at'] = datetime.now().isoformat()
            
            connections[business_id] = connection_data
            
            return self._save_json_file(self.facebook_connections_file, connections)
            
        except Exception as e:
            print(f"Error storing Facebook connection: {e}")
            return False
    
    def get_facebook_connection(self, business_id: str) -> Optional[Dict]:
        """Retrieve Facebook connection for a business"""
        try:
            connections = self._load_json_file(self.facebook_connections_file)
            return connections.get(business_id)
            
        except Exception as e:
            print(f"Error retrieving Facebook connection: {e}")
            return None
    
    def update_facebook_connection(self, business_id: str, updates: Dict) -> bool:
        """Update Facebook connection"""
        try:
            connections = self._load_json_file(self.facebook_connections_file)
            
            if business_id not in connections:
                return False
            
            connections[business_id].update(updates)
            connections[business_id]['updated_at'] = datetime.now().isoformat()
            
            return self._save_json_file(self.facebook_connections_file, connections)
            
        except Exception as e:
            print(f"Error updating Facebook connection: {e}")
            return False
    
    def delete_facebook_connection(self, business_id: str) -> bool:
        """Delete Facebook connection"""
        try:
            connections = self._load_json_file(self.facebook_connections_file)
            
            if business_id in connections:
                del connections[business_id]
                return self._save_json_file(self.facebook_connections_file, connections)
            
            return False
            
        except Exception as e:
            print(f"Error deleting Facebook connection: {e}")
            return False
    
    # =====================================
    # Utility Operations
    # =====================================
    
    def get_analytics_data(self, business_id: str = None) -> Dict:
        """Get analytics data for dashboard"""
        try:
            posts = self._load_json_file(self.posts_file)
            profiles = self._load_json_file(self.business_profiles_file)
            schedules = self._load_json_file(self.schedules_file)
            
            # Filter by business if specified
            if business_id:
                business_posts = [p for p in posts.values() if p.get('business_id') == business_id]
                business_count = 1 if business_id in profiles else 0
                business_schedules = [s for s in schedules.values() if s.get('business_id') == business_id]
            else:
                business_posts = list(posts.values())
                business_count = len(profiles)
                business_schedules = list(schedules.values())
            
            # Calculate statistics
            total_posts = len(business_posts)
            published_posts = len([p for p in business_posts if p.get('status') == 'published'])
            scheduled_posts = len([p for p in business_posts if p.get('status') == 'scheduled'])
            draft_posts = len([p for p in business_posts if p.get('status') == 'draft'])
            
            # Post types distribution
            post_types = {}
            for post in business_posts:
                post_type = post.get('post_type', 'unknown')
                post_types[post_type] = post_types.get(post_type, 0) + 1
            
            return {
                'total_businesses': business_count,
                'total_posts': total_posts,
                'published_posts': published_posts,
                'scheduled_posts': scheduled_posts,
                'draft_posts': draft_posts,
                'total_schedules': len(business_schedules),
                'post_types_distribution': post_types,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating analytics data: {e}")
            return {}
    
    def cleanup_old_data(self, days_old: int = 30) -> Dict:
        """Clean up old data (drafts, completed schedules, etc.)"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
            cleanup_stats = {
                'deleted_posts': 0,
                'deleted_schedules': 0
            }
            
            # Clean up old draft posts
            posts = self._load_json_file(self.posts_file)
            posts_to_delete = []
            
            for post_id, post in posts.items():
                if (post.get('status') == 'draft' and 
                    post.get('created_at', '') < cutoff_date):
                    posts_to_delete.append(post_id)
            
            for post_id in posts_to_delete:
                del posts[post_id]
                cleanup_stats['deleted_posts'] += 1
            
            self._save_json_file(self.posts_file, posts)
            
            # Clean up old schedules
            schedules = self._load_json_file(self.schedules_file)
            schedules_to_delete = []
            
            for schedule_id, schedule in schedules.items():
                if schedule.get('created_at', '') < cutoff_date:
                    schedules_to_delete.append(schedule_id)
            
            for schedule_id in schedules_to_delete:
                del schedules[schedule_id]
                cleanup_stats['deleted_schedules'] += 1
            
            self._save_json_file(self.schedules_file, schedules)
            
            cleanup_stats['cleanup_completed_at'] = datetime.now().isoformat()
            return cleanup_stats
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return {'error': str(e)}
    
    def export_data(self, business_id: str = None) -> Dict:
        """Export data for backup or migration"""
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'business_id': business_id
            }
            
            if business_id:
                # Export specific business data
                export_data['business_profile'] = self.get_business_profile(business_id)
                export_data['posts'] = self.get_posts_by_business(business_id)
                export_data['schedules'] = self.get_schedules_by_business(business_id)
                export_data['facebook_connection'] = self.get_facebook_connection(business_id)
            else:
                # Export all data
                export_data['business_profiles'] = self._load_json_file(self.business_profiles_file)
                export_data['posts'] = self._load_json_file(self.posts_file)
                export_data['schedules'] = self._load_json_file(self.schedules_file)
                export_data['facebook_connections'] = self._load_json_file(self.facebook_connections_file)
            
            return export_data
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return {'error': str(e)}
    
    # =====================================
    # Private Helper Methods
    # =====================================
    
    def _load_json_file(self, file_path: str) -> Dict:
        """Load data from JSON file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json_file(self, file_path: str, data: Dict) -> bool:
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error saving to {file_path}: {e}")
            return False

# Test function
def test_data_storage():
    """Test the data storage functionality"""
    storage = DataStorage('test_data')
    
    # Test business profile operations
    print("Testing business profile operations...")
    
    business_id = str(uuid.uuid4())
    business_profile = {
        'business_name': 'Test Gym',
        'industry': 'fitness',
        'website_url': 'https://testgym.com',
        'description': 'A test fitness center'
    }
    
    # Store
    success = storage.store_business_profile(business_id, business_profile)
    print(f"Store business profile: {success}")
    
    # Retrieve
    retrieved = storage.get_business_profile(business_id)
    print(f"Retrieved business profile: {retrieved['business_name'] if retrieved else 'None'}")
    
    # Test post operations
    print("\nTesting post operations...")
    
    post_id = str(uuid.uuid4())
    post = {
        'business_id': business_id,
        'content': 'Test post content',
        'post_type': 'promo',
        'status': 'draft'
    }
    
    # Store
    success = storage.store_post(post_id, post)
    print(f"Store post: {success}")
    
    # Retrieve
    retrieved_post = storage.get_post(post_id)
    print(f"Retrieved post: {retrieved_post['content'] if retrieved_post else 'None'}")
    
    # Get posts by business
    business_posts = storage.get_posts_by_business(business_id)
    print(f"Posts for business: {len(business_posts)}")
    
    # Test analytics
    print("\nTesting analytics...")
    analytics = storage.get_analytics_data(business_id)
    print(f"Analytics: {analytics}")
    
    print("\nData storage tests completed!")

if __name__ == "__main__":
    test_data_storage()