
import requests
import sys
import os
import json
from datetime import datetime

class RelocateMeAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        if not headers:
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

    def test_login(self, username, password):
        """Test login and get token"""
        success, response = self.run_test(
            "Login with noir-themed hacking credentials",
            "POST",
            "api/auth/login",
            200,
            data={"username": username, "password": password}
        )
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_user_info(self):
        """Test getting user info with token"""
        success, response = self.run_test(
            "Get user info with token",
            "GET",
            "api/auth/me",
            200
        )
        return success

    def test_timeline(self):
        """Test getting timeline data"""
        success, response = self.run_test(
            "Get timeline data",
            "GET",
            "api/timeline/full",
            200
        )
        return success

    def test_visa_requirements(self):
        """Test getting visa requirements"""
        success, response = self.run_test(
            "Get visa requirements",
            "GET",
            "api/visa/requirements",
            200
        )
        return success

    def test_job_listings(self):
        """Test getting job listings"""
        success, response = self.run_test(
            "Get job listings",
            "GET",
            "api/jobs/listings",
            200
        )
        return success

def main():
    # Get the backend URL from environment or use the one from frontend/.env
    backend_url = "https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com"
    
    # Setup tester
    tester = RelocateMeAPITester(backend_url)
    
    # Test credentials from the noir-themed hacking animation
    username = "relocate_user"
    password = "SecurePass2025!"

    print(f"\n🔒 Testing Noir-Themed Hacking Animation Authentication API")
    print(f"🌐 Backend URL: {backend_url}")
    print(f"👤 Using credentials discovered in the hacking animation: {username}/{password}")
    
    # Run tests
    if not tester.test_login(username, password):
        print("❌ Login failed with the credentials from the noir-themed hacking animation")
        return 1

    print("✅ Successfully authenticated with the credentials from the noir-themed hacking animation")
    
    # Test protected endpoints
    tester.test_user_info()
    tester.test_timeline()
    tester.test_visa_requirements()
    tester.test_job_listings()

    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
