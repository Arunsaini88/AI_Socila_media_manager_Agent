# test_complete_system.py
"""
Complete system test script for AI Social Media Manager Backend
Tests all components and API endpoints to ensure everything works correctly
"""

import requests
import json
import time
from datetime import datetime
import sys

class SystemTester:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        
        # Test data storage
        self.business_id = None
        self.post_ids = []
        self.schedule_id = None
        
        # Test results
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
    
    def log_test(self, test_name, success, message="", data=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {test_name}")
        if message:
            print(f"     {message}")
        if data and not success:
            print(f"     Data: {json.dumps(data, indent=2)[:200]}...")
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        if success:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        print()
    
    def test_health_check(self):
        """Test API health endpoint"""
        print("🏥 Testing Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Health Check", True, "API is healthy and responding")
                    return True
                else:
                    self.log_test("Health Check", False, "API responded but reported unhealthy")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
        
        return False
    
    def test_business_analysis(self):
        """Test business website analysis"""
        print("🏢 Testing Business Analysis...")
        
        test_websites = [
            "https://www.planetfitness.com",
            "https://example.com",  # This will test error handling
        ]
        
        for website in test_websites:
            try:
                payload = {"website_url": website}
                response = self.session.post(f"{self.base_url}/business/analyze", 
                                           json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('business_id'):
                        # Store first successful business ID for later tests
                        if not self.business_id:
                            self.business_id = data['business_id']
                        
                        profile = data.get('profile', {})
                        self.log_test(f"Business Analysis - {website}", True, 
                                    f"Business: {profile.get('business_name', 'Unknown')}, "
                                    f"Industry: {profile.get('industry', 'Unknown')}")
                    else:
                        self.log_test(f"Business Analysis - {website}", False, 
                                    f"Analysis failed: {data.get('error', 'Unknown error')}")
                else:
                    self.log_test(f"Business Analysis - {website}", False, 
                                f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Business Analysis - {website}", False, str(e))
        
        # Test retrieving business profile
        if self.business_id:
            try:
                response = self.session.get(f"{self.base_url}/business/{self.business_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("Get Business Profile", True, 
                                    f"Retrieved profile for business ID: {self.business_id}")
                    else:
                        self.log_test("Get Business Profile", False, "Profile not found")
                else:
                    self.log_test("Get Business Profile", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Get Business Profile", False, str(e))
    
    def test_industry_news(self):
        """Test industry news analysis"""
        print("📰 Testing Industry News Analysis...")
        
        test_industries = [
            {"industry": "fitness", "keywords": ["gym", "workout"]},
            {"industry": "beauty", "keywords": ["salon", "spa"]},
            {"industry": "food", "keywords": ["restaurant"]},
            {"industry": "general", "keywords": []},
        ]
        
        for test_case in test_industries:
            try:
                response = self.session.post(f"{self.base_url}/news/analyze", 
                                           json=test_case)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        insights = data.get('insights', [])
                        self.log_test(f"Industry News - {test_case['industry']}", True, 
                                    f"Retrieved {len(insights)} news insights")
                    else:
                        self.log_test(f"Industry News - {test_case['industry']}", False, 
                                    data.get('error', 'Unknown error'))
                else:
                    self.log_test(f"Industry News - {test_case['industry']}", False, 
                                f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Industry News - {test_case['industry']}", False, str(e))
    
    def test_content_generation(self):
        """Test AI content generation"""
        print("✍️ Testing Content Generation...")
        
        if not self.business_id:
            self.log_test("Content Generation", False, "No business ID available from previous tests")
            return
        
        test_preferences = [
            {
                "tone": "friendly",
                "frequency": 3,
                "post_types": ["promo", "tip", "insight"]
            },
            {
                "tone": "professional", 
                "frequency": 2,
                "post_types": ["promo", "update"]
            },
            {
                "tone": "casual",
                "frequency": 1,
                "post_types": ["tip"]
            }
        ]
        
        for prefs in test_preferences:
            try:
                payload = {
                    "business_id": self.business_id,
                    "post_preferences": prefs
                }
                
                response = self.session.post(f"{self.base_url}/content/generate", 
                                           json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        posts = data.get('posts', [])
                        # Store post IDs for later tests
                        for post in posts:
                            if post.get('id'):
                                self.post_ids.append(post['id'])
                        
                        self.log_test(f"Content Generation - {prefs['tone']}", True, 
                                    f"Generated {len(posts)} posts")
                    else:
                        self.log_test(f"Content Generation - {prefs['tone']}", False, 
                                    data.get('error', 'Unknown error'))
                else:
                    self.log_test(f"Content Generation - {prefs['tone']}", False, 
                                f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Content Generation - {prefs['tone']}", False, str(e))
    
    def test_weekly_scheduling(self):
        """Test weekly schedule creation"""
        print("📅 Testing Weekly Scheduling...")
        
        if not self.business_id:
            self.log_test("Weekly Scheduling", False, "No business ID available")
            return
        
        schedule_configs = [
            {
                "frequency": 3,
                "preferred_days": ["monday", "wednesday", "friday"]
            },
            {
                "frequency": 2,
                "preferred_days": ["tuesday", "thursday"]
            }
        ]
        
        for config in schedule_configs:
            try:
                payload = {
                    "business_id": self.business_id,
                    "start_date": "2025-08-04",
                    **config
                }
                
                response = self.session.post(f"{self.base_url}/planner/schedule", 
                                           json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        if not self.schedule_id:
                            self.schedule_id = data.get('schedule_id')
                        
                        schedule = data.get('schedule', {})
                        scheduled_days = sum(1 for day_info in schedule.values() 
                                           if day_info.get('post'))
                        
                        self.log_test(f"Weekly Schedule - {config['frequency']} posts", True, 
                                    f"Created schedule with {scheduled_days} scheduled days")
                    else:
                        self.log_test(f"Weekly Schedule - {config['frequency']} posts", False, 
                                    data.get('error', 'Unknown error'))
                else:
                    self.log_test(f"Weekly Schedule - {config['frequency']} posts", False, 
                                f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test(f"Weekly Schedule - {config['frequency']} posts", False, str(e))
        
        # Test retrieving schedule
        if self.schedule_id:
            try:
                response = self.session.get(f"{self.base_url}/planner/schedule/{self.schedule_id}")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("Get Schedule", True, "Retrieved schedule successfully")
                    else:
                        self.log_test("Get Schedule", False, "Schedule not found")
                else:
                    self.log_test("Get Schedule", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Get Schedule", False, str(e))
    
    def test_post_management(self):
        """Test post editing and management"""
        print("📝 Testing Post Management...")
        
        if not self.business_id:
            self.log_test("Post Management", False, "No business ID available")
            return
        
        # Test getting all posts for business
        try:
            response = self.session.get(f"{self.base_url}/business/{self.business_id}/posts")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    posts = data.get('posts', [])
                    self.log_test("Get Business Posts", True, f"Retrieved {len(posts)} posts")
                else:
                    self.log_test("Get Business Posts", False, "Failed to get posts")
            else:
                self.log_test("Get Business Posts", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Business Posts", False, str(e))
        
        # Test getting scheduled posts
        try:
            response = self.session.get(f"{self.base_url}/posts/scheduled/{self.business_id}")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    posts = data.get('posts', [])
                    self.log_test("Get Scheduled Posts", True, f"Retrieved {len(posts)} scheduled posts")
                else:
                    self.log_test("Get Scheduled Posts", False, "Failed to get scheduled posts")
            else:
                self.log_test("Get Scheduled Posts", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Scheduled Posts", False, str(e))
        
        # Test updating a post
        if self.post_ids:
            post_id = self.post_ids[0]
            try:
                update_payload = {
                    "content": "Updated test content! 🚀",
                    "hashtags": ["#updated", "#test", "#awesome"]
                }
                
                response = self.session.put(f"{self.base_url}/posts/{post_id}", 
                                          json=update_payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_test("Update Post", True, f"Updated post {post_id}")
                    else:
                        self.log_test("Update Post", False, "Update failed")
                else:
                    self.log_test("Update Post", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Update Post", False, str(e))
    
    def test_facebook_integration(self):
        """Test Facebook integration (mock mode)"""
        print("📘 Testing Facebook Integration...")
        
        # Test connecting Facebook page
        try:
            payload = {"access_token": "mock-user-access-token"}
            response = self.session.post(f"{self.base_url}/facebook/connect", 
                                       json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    connection = data.get('connection', {})
                    page = connection.get('page', {})
                    self.log_test("Facebook Connection", True, 
                                f"Connected to page: {page.get('name', 'Unknown')}")
                else:
                    self.log_test("Facebook Connection", False, 
                                data.get('error', 'Connection failed'))
            else:
                self.log_test("Facebook Connection", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Facebook Connection", False, str(e))
        
        # Test getting Facebook pages
        try:
            headers = {"Authorization": "Bearer mock-user-access-token"}
            response = self.session.get(f"{self.base_url}/facebook/pages", 
                                      headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pages = data.get('pages', [])
                    self.log_test("Get Facebook Pages", True, 
                                f"Retrieved {len(pages)} pages")
                else:
                    self.log_test("Get Facebook Pages", False, "Failed to get pages")
            else:
                self.log_test("Get Facebook Pages", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Facebook Pages", False, str(e))
        
        # Test publishing a post
        if self.post_ids:
            post_id = self.post_ids[0]
            try:
                publish_payload = {
                    "page_id": "123456789",
                    "access_token": "mock-page-token-123"
                }
                
                response = self.session.post(f"{self.base_url}/posts/{post_id}/publish", 
                                           json=publish_payload)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        facebook_result = data.get('facebook_result', {})
                        post_url = facebook_result.get('post_url', 'Unknown')
                        self.log_test("Publish Post", True, 
                                    f"Published successfully: {post_url}")
                    else:
                        self.log_test("Publish Post", False, 
                                    data.get('error', 'Publish failed'))
                else:
                    self.log_test("Publish Post", False, f"HTTP {response.status_code}")
            except Exception as e:
                self.log_test("Publish Post", False, str(e))
    
    def test_complete_workflow(self):
        """Test a complete end-to-end workflow"""
        print("🔄 Testing Complete Workflow...")
        
        workflow_business_id = None
        workflow_post_id = None
        
        # Step 1: Analyze business
        try:
            payload = {"website_url": "https://example-salon.com"}
            response = self.session.post(f"{self.base_url}/business/analyze", 
                                       json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    workflow_business_id = data['business_id']
                    self.log_test("Workflow Step 1 - Business Analysis", True, 
                                "Business analyzed successfully")
                else:
                    self.log_test("Workflow Step 1 - Business Analysis", False, 
                                "Analysis failed")
                    return
            else:
                self.log_test("Workflow Step 1 - Business Analysis", False, 
                            f"HTTP {response.status_code}")
                return
        except Exception as e:
            self.log_test("Workflow Step 1 - Business Analysis", False, str(e))
            return
        
        # Step 2: Generate content
        try:
            payload = {
                "business_id": workflow_business_id,
                "post_preferences": {
                    "tone": "friendly",
                    "frequency": 1,
                    "post_types": ["promo"]
                }
            }
            
            response = self.session.post(f"{self.base_url}/content/generate", 
                                       json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('posts'):
                    workflow_post_id = data['posts'][0]['id']
                    self.log_test("Workflow Step 2 - Content Generation", True, 
                                "Content generated successfully")
                else:
                    self.log_test("Workflow Step 2 - Content Generation", False, 
                                "Generation failed")
                    return
            else:
                self.log_test("Workflow Step 2 - Content Generation", False, 
                            f"HTTP {response.status_code}")
                return
        except Exception as e:
            self.log_test("Workflow Step 2 - Content Generation", False, str(e))
            return
        
        # Step 3: Publish post
        try:
            payload = {
                "page_id": "123456789",
                "access_token": "mock-page-token-123"
            }
            
            response = self.session.post(f"{self.base_url}/posts/{workflow_post_id}/publish", 
                                       json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_test("Workflow Step 3 - Publish Post", True, 
                                "Post published successfully")
                    self.log_test("Complete Workflow", True, 
                                "✨ End-to-end workflow completed successfully!")
                else:
                    self.log_test("Workflow Step 3 - Publish Post", False, 
                                "Publish failed")
            else:
                self.log_test("Workflow Step 3 - Publish Post", False, 
                            f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Workflow Step 3 - Publish Post", False, str(e))
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting Complete System Test...")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        if not self.test_health_check():
            print("❌ API is not responding. Please start the server first.")
            return False
        
        self.test_business_analysis()
        self.test_industry_news()
        self.test_content_generation()
        self.test_weekly_scheduling()
        self.test_post_management()
        self.test_facebook_integration()
        self.test_complete_workflow()
        
        # Print summary
        end_time = time.time()
        duration = end_time - start_time
        
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.passed_tests + self.failed_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📈 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! The system is working correctly.")
        else:
            print(f"\n⚠️  {self.failed_tests} tests failed. Please check the logs above.")
        
        return self.failed_tests == 0
    
    def save_test_report(self, filename="test_report.json"):
        """Save detailed test report to file"""
        report = {
            "summary": {
                "total_tests": self.passed_tests + self.failed_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "success_rate": (self.passed_tests / (self.passed_tests + self.failed_tests) * 100) if (self.passed_tests + self.failed_tests) > 0 else 0,
                "test_date": datetime.now().isoformat()
            },
            "results": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Test report saved to {filename}")

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Social Media Manager System Tester')
    parser.add_argument('--url', default='http://localhost:5000/api', 
                       help='Base API URL (default: http://localhost:5000/api)')
    parser.add_argument('--report', default='test_report.json',
                       help='Test report filename (default: test_report.json)')
    
    args = parser.parse_args()
    
    # Create tester instance
    tester = SystemTester(args.url)
    
    # Run tests
    success = tester.run_all_tests()
    
    # Save report
    tester.save_test_report(args.report)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()