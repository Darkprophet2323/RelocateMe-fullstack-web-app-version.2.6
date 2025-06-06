
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

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
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
                    return success, response.json()
                except:
                    return success, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    print(f"Response: {response.json()}")
                except:
                    print(f"Response: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_login(self, username="relocate_user", password="SecurePass2025!"):
        """Test login and get token"""
        success, response = self.run_test(
            "Login",
            "POST",
            "auth/login",
            200,
            data={"username": username, "password": password}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_user_info(self):
        """Test getting user info"""
        return self.run_test(
            "Get User Info",
            "GET",
            "auth/me",
            200
        )

    def test_get_timeline(self):
        """Test getting timeline data"""
        return self.run_test(
            "Get Timeline",
            "GET",
            "timeline/full",
            200
        )

    def test_get_progress_items(self):
        """Test getting progress items"""
        return self.run_test(
            "Get Progress Items",
            "GET",
            "progress/items",
            200
        )

    def test_get_visa_requirements(self):
        """Test getting visa requirements"""
        return self.run_test(
            "Get Visa Requirements",
            "GET",
            "visa/requirements",
            200
        )

    def test_get_job_listings(self):
        """Test getting job listings"""
        return self.run_test(
            "Get Job Listings",
            "GET",
            "jobs/listings",
            200
        )

    def test_get_resources(self):
        """Test getting resources"""
        return self.run_test(
            "Get Resources",
            "GET",
            "resources/all",
            200
        )

def main():
    # Setup
    tester = RelocateMeAPITester()
    
    # Run tests
    if not tester.test_login():
        print("❌ Login failed, stopping tests")
        return 1

    # Test user info
    tester.test_get_user_info()
    
    # Test timeline
    tester.test_get_timeline()
    
    # Test progress items
    tester.test_get_progress_items()
    
    # Test visa requirements
    tester.test_get_visa_requirements()
    
    # Test job listings
    tester.test_get_job_listings()
    
    # Test resources
    tester.test_get_resources()

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
