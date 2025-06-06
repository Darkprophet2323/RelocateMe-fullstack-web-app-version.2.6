
import requests
import sys
import json
from datetime import datetime

class RelocateMeAPITester:
    def __init__(self, base_url="https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = {}

    def run_test(self, name, method, endpoint, expected_status, data=None, auth=True):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if auth and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
            
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    result = response.json()
                    print(f"   Response preview: {json.dumps(result, indent=2)[:200]}...")
                except:
                    result = {"message": "No JSON response"}
                    print(f"   Response: {result}")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    result = response.json()
                    print(f"   Error response: {json.dumps(result, indent=2)[:200]}...")
                except:
                    result = {"error": "No JSON response"}
                    print(f"   Error: {result}")
            
            self.test_results[name] = {
                "success": success,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "response": result
            }
            
            return success, result

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results[name] = {
                "success": False,
                "error": str(e)
            }
            return False, {"error": str(e)}

    # Authentication Tests
    def test_login(self):
        """Test login functionality"""
        return self.run_test(
            "Login",
            "POST",
            "auth/login",
            200,
            data={"username": "relocate_user", "password": "SecurePass2025!"},
            auth=False
        )
    
    def test_get_user_profile(self):
        """Test user profile retrieval"""
        return self.run_test(
            "Get User Profile",
            "GET",
            "auth/me",
            200
        )
    
    def test_password_reset_request(self):
        """Test password reset request"""
        return self.run_test(
            "Password Reset Request",
            "POST",
            "auth/reset-password",
            200,
            data={"username": "relocate_user"},
            auth=False
        )

    # Timeline Tests
    def test_get_timeline(self):
        """Test timeline retrieval"""
        return self.run_test(
            "Get Timeline",
            "GET",
            "timeline/full",
            200
        )
    
    def test_get_timeline_by_category(self):
        """Test timeline by category retrieval"""
        return self.run_test(
            "Get Timeline By Category",
            "GET",
            "timeline/by-category",
            200
        )
    
    def test_update_timeline_progress(self):
        """Test updating timeline progress"""
        return self.run_test(
            "Update Timeline Progress",
            "POST",
            "timeline/update-progress",
            200,
            data={"step_id": 1, "completed": True, "notes": "Test note"}
        )
    
    # Visa Tests
    def test_get_visa_requirements(self):
        """Test visa requirements retrieval"""
        return self.run_test(
            "Get Visa Requirements",
            "GET",
            "visa/requirements",
            200,
            auth=False
        )
    
    def test_get_visa_checklist(self):
        """Test visa checklist retrieval"""
        return self.run_test(
            "Get Visa Checklist",
            "GET",
            "visa/checklist",
            200,
            auth=False
        )
    
    def test_get_specific_visa_requirement(self):
        """Test specific visa requirement retrieval"""
        return self.run_test(
            "Get Specific Visa Requirement",
            "GET",
            "visa/requirements/skilled-worker-visa",
            200,
            auth=False
        )
    
    # Job Listings Tests
    def test_get_job_listings(self):
        """Test job listings retrieval"""
        return self.run_test(
            "Get Job Listings",
            "GET",
            "jobs/listings",
            200,
            auth=False
        )
    
    def test_get_job_listings_with_filters(self):
        """Test job listings with filters"""
        return self.run_test(
            "Get Job Listings With Filters",
            "GET",
            "jobs/listings?category=Technology&job_type=remote",
            200,
            auth=False
        )
    
    def test_get_job_categories(self):
        """Test job categories retrieval"""
        return self.run_test(
            "Get Job Categories",
            "GET",
            "jobs/categories",
            200,
            auth=False
        )
    
    def test_get_featured_jobs(self):
        """Test featured jobs retrieval"""
        return self.run_test(
            "Get Featured Jobs",
            "GET",
            "jobs/featured",
            200,
            auth=False
        )
    
    # Progress Tracking Tests
    def test_get_progress_items(self):
        """Test progress items retrieval"""
        return self.run_test(
            "Get Progress Items",
            "GET",
            "progress/items",
            200
        )
    
    def test_get_progress_items_with_filters(self):
        """Test progress items with filters"""
        return self.run_test(
            "Get Progress Items With Filters",
            "GET",
            "progress/items?category=Documentation&status=completed",
            200
        )
    
    def test_get_progress_dashboard(self):
        """Test progress dashboard retrieval"""
        return self.run_test(
            "Get Progress Dashboard",
            "GET",
            "progress/dashboard",
            200
        )
    
    def test_update_progress_item(self):
        """Test updating progress item"""
        # First get progress items to find an ID
        success, items_response = self.run_test(
            "Get Progress Item ID",
            "GET",
            "progress/items",
            200
        )
        
        if success and "items" in items_response and len(items_response["items"]) > 0:
            item_id = items_response["items"][0]["id"]
            return self.run_test(
                "Update Progress Item",
                "PUT",
                f"progress/items/{item_id}",
                200,
                data={"status": "in_progress", "notes": "Updated via API test"}
            )
        else:
            print("❌ Could not find progress item ID for update test")
            self.test_results["Update Progress Item"] = {
                "success": False,
                "error": "No progress items found to update"
            }
            return False, {"error": "No progress items found"}
    
    def test_toggle_subtask(self):
        """Test toggling a subtask"""
        # First get progress items to find an ID with subtasks
        success, items_response = self.run_test(
            "Get Progress Item with Subtasks",
            "GET",
            "progress/items",
            200
        )
        
        if success and "items" in items_response and len(items_response["items"]) > 0:
            # Find an item with subtasks
            for item in items_response["items"]:
                if "subtasks" in item and len(item["subtasks"]) > 0:
                    item_id = item["id"]
                    return self.run_test(
                        "Toggle Subtask",
                        "POST",
                        f"progress/items/{item_id}/subtasks/0/toggle",
                        200
                    )
            
            print("❌ Could not find progress item with subtasks for toggle test")
            self.test_results["Toggle Subtask"] = {
                "success": False,
                "error": "No progress items with subtasks found"
            }
            return False, {"error": "No subtasks found"}
        else:
            print("❌ Could not find progress items for subtask toggle test")
            self.test_results["Toggle Subtask"] = {
                "success": False,
                "error": "No progress items found"
            }
            return False, {"error": "No progress items found"}
    
    # Resources Tests
    def test_get_resources(self):
        """Test resources retrieval"""
        return self.run_test(
            "Get Resources",
            "GET",
            "resources/all",
            200,
            auth=False
        )
    
    # Logistics Tests
    def test_get_logistics_providers(self):
        """Test logistics providers retrieval"""
        return self.run_test(
            "Get Logistics Providers",
            "GET",
            "logistics/providers",
            200,
            auth=False
        )
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print(f"📊 RELOCATEME API TEST SUMMARY: {self.tests_passed}/{self.tests_run} tests passed ({(self.tests_passed/self.tests_run)*100 if self.tests_run > 0 else 0:.1f}%)")
        print("="*80)
        
        # Group tests by category
        categories = {
            "Authentication": ["Login", "Get User Profile", "Password Reset Request"],
            "Timeline": ["Get Timeline", "Get Timeline By Category", "Update Timeline Progress"],
            "Visa": ["Get Visa Requirements", "Get Visa Checklist", "Get Specific Visa Requirement"],
            "Jobs": ["Get Job Listings", "Get Job Listings With Filters", "Get Job Categories", "Get Featured Jobs"],
            "Progress": ["Get Progress Items", "Get Progress Items With Filters", "Get Progress Dashboard", "Update Progress Item", "Toggle Subtask"],
            "Resources": ["Get Resources"],
            "Logistics": ["Get Logistics Providers"]
        }
        
        # Print summary by category
        for category, test_names in categories.items():
            category_tests = [name for name in test_names if name in self.test_results]
            if not category_tests:
                continue
                
            passed = sum(1 for name in category_tests if self.test_results.get(name, {}).get("success", False))
            total = len(category_tests)
            
            if passed == total:
                status = "✅"
            elif passed > 0:
                status = "⚠️"
            else:
                status = "❌"
                
            print(f"{status} {category}: {passed}/{total} passed")
        
        # Print details of failed tests
        failed_tests = {name: details for name, details in self.test_results.items() if not details["success"]}
        if failed_tests:
            print("\n❌ FAILED TESTS DETAILS:")
            for name, details in failed_tests.items():
                print(f"  - {name}:")
                if "error" in details:
                    print(f"    Error: {details['error']}")
                else:
                    print(f"    Expected status: {details['expected_status']}, Got: {details['status_code']}")
                    if "response" in details:
                        print(f"    Response: {json.dumps(details['response'], indent=2)[:200]}...")
        
        return self.tests_passed == self.tests_run

def main():
    print("🚀 Starting RelocateMe API Tests")
    print("="*80)
    print(f"🌐 Testing against: https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com")
    print("="*80)
    
    tester = RelocateMeAPITester()
    
    # Test authentication
    login_success, login_response = tester.test_login()
    if login_success and "access_token" in login_response:
        tester.token = login_response["access_token"]
        print(f"✅ Authentication successful, token received")
    else:
        print(f"❌ Authentication failed, continuing with unauthenticated tests")
    
    # Test API endpoints that don't require authentication
    tester.test_get_visa_requirements()
    tester.test_get_visa_checklist()
    tester.test_get_specific_visa_requirement()
    tester.test_get_job_listings()
    tester.test_get_job_listings_with_filters()
    tester.test_get_job_categories()
    tester.test_get_featured_jobs()
    tester.test_get_resources()
    tester.test_get_logistics_providers()
    tester.test_password_reset_request()
    
    # Tests requiring authentication
    if tester.token:
        tester.test_get_user_profile()
        tester.test_get_timeline()
        tester.test_get_timeline_by_category()
        tester.test_update_timeline_progress()
        tester.test_get_progress_items()
        tester.test_get_progress_items_with_filters()
        tester.test_get_progress_dashboard()
        tester.test_update_progress_item()
        tester.test_toggle_subtask()
    
    # Print summary
    success = tester.print_summary()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
