
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
            
            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    result = response.json()
                except:
                    result = {"message": "No JSON response"}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    result = response.json()
                except:
                    result = {"error": "No JSON response"}
            
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

    def test_get_timeline(self):
        """Test timeline retrieval"""
        return self.run_test(
            "Get Timeline",
            "GET",
            "timeline/full",
            200
        )
    
    def test_get_visa_requirements(self):
        """Test visa requirements retrieval"""
        return self.run_test(
            "Get Visa Requirements",
            "GET",
            "visa/requirements",
            200,
            auth=False
        )
    
    def test_get_job_listings(self):
        """Test job listings retrieval"""
        return self.run_test(
            "Get Job Listings",
            "GET",
            "jobs/listings",
            200,
            auth=False
        )
    
    def test_get_progress_items(self):
        """Test progress items retrieval"""
        return self.run_test(
            "Get Progress Items",
            "GET",
            "progress/items",
            200
        )
    
    def test_get_dashboard_overview(self):
        """Test dashboard overview retrieval"""
        return self.run_test(
            "Get Dashboard Overview",
            "GET",
            "dashboard/overview",
            200,
            auth=False
        )
    
    def test_update_progress(self):
        """Test updating progress"""
        return self.run_test(
            "Update Progress",
            "POST",
            "timeline/update-progress",
            200,
            data={"step_id": 1, "completed": True}
        )
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print(f"📊 API TEST SUMMARY: {self.tests_passed}/{self.tests_run} tests passed ({(self.tests_passed/self.tests_run)*100 if self.tests_run > 0 else 0:.1f}%)")
        print("="*50)
        
        # Print details of failed tests
        failed_tests = {name: details for name, details in self.test_results.items() if not details["success"]}
        if failed_tests:
            print("\n❌ FAILED TESTS:")
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
    print("="*50)
    
    tester = RelocateMeAPITester()
    
    # Test authentication
    login_success, login_response = tester.test_login()
    if login_success and "access_token" in login_response:
        tester.token = login_response["access_token"]
        print(f"✅ Authentication successful, token received")
    else:
        print(f"❌ Authentication failed, continuing with unauthenticated tests")
    
    # Test API endpoints
    tester.test_get_visa_requirements()
    tester.test_get_job_listings()
    
    # Tests requiring authentication
    if tester.token:
        tester.test_get_timeline()
        tester.test_get_progress_items()
        tester.test_update_progress()
    
    # Test dashboard overview (may or may not require auth)
    tester.test_get_dashboard_overview()
    
    # Print summary
    success = tester.print_summary()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
