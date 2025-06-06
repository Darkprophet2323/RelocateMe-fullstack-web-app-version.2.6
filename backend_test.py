import requests
import sys
import json
import time

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
            "Login with hacked credentials",
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
        if not self.token:
            print("❌ No token available, skipping user info test")
            return False
        
        success, response = self.run_test(
            "Get user info",
            "GET",
            "api/auth/me",
            200
        )
        return success

    def test_timeline(self):
        """Test getting timeline data"""
        if not self.token:
            print("❌ No token available, skipping timeline test")
            return False
        
        success, response = self.run_test(
            "Get timeline data",
            "GET",
            "api/timeline/full",
            200
        )
        return success

def main():
    # Get the backend URL from the command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com"
    
    print(f"Testing API at: {base_url}")
    
    # Setup tester
    tester = RelocateMeAPITester(base_url)
    
    # Test login with the "hacked" credentials from the login animation
    username = "relocate_user"
    password = "SecurePass2025!"
    
    print(f"\n🔐 Testing login with credentials discovered in the hacking animation:")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    
    if not tester.test_login(username, password):
        print("❌ Login failed, stopping tests")
        return 1
    
    print("✅ Login successful! Token received.")
    
    # Test getting user info
    if not tester.test_user_info():
        print("❌ Getting user info failed")
    else:
        print("✅ Successfully retrieved user info")
    
    # Test getting timeline data
    if not tester.test_timeline():
        print("❌ Getting timeline data failed")
    else:
        print("✅ Successfully retrieved timeline data")
    
    # Print results
    print(f"\n📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())
