
import requests
import sys
import time
from datetime import datetime

class RelocateMeAPITester:
    def __init__(self, base_url="https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.username = "relocate_user"
        self.password = "SecurePass2025!"

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params)
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

    def test_login(self):
        """Test login and get token"""
        success, response = self.run_test(
            "Login",
            "POST",
            "auth/login",
            200,
            data={"username": self.username, "password": self.password}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            print(f"✅ Successfully logged in as {self.username}")
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

    def test_get_timeline_by_category(self):
        """Test getting timeline data by category"""
        return self.run_test(
            "Get Timeline By Category",
            "GET",
            "timeline/by-category",
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

    def test_get_progress_dashboard(self):
        """Test getting progress dashboard"""
        return self.run_test(
            "Get Progress Dashboard",
            "GET",
            "progress/dashboard",
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

    def test_get_job_categories(self):
        """Test getting job categories"""
        return self.run_test(
            "Get Job Categories",
            "GET",
            "jobs/categories",
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

    def test_get_visa_checklist(self):
        """Test getting visa checklist"""
        return self.run_test(
            "Get Visa Checklist",
            "GET",
            "visa/checklist",
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
    
    # Run login test first
    if not tester.test_login():
        print("❌ Login failed, stopping tests")
        return 1

    # Run other tests
    tester.test_get_user_info()
    tester.test_get_timeline()
    tester.test_get_timeline_by_category()
    tester.test_get_progress_items()
    tester.test_get_progress_dashboard()
    tester.test_get_job_listings()
    tester.test_get_job_categories()
    tester.test_get_visa_requirements()
    tester.test_get_visa_checklist()
    tester.test_get_resources()

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
