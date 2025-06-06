import requests
import unittest
import json
from datetime import datetime

class RelocateMeAPITester:
    def __init__(self, base_url="https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            
            status_success = response.status_code == expected_status
            
            if status_success:
                self.tests_passed += 1
                result = {
                    "name": name,
                    "status": "PASS",
                    "response_code": response.status_code,
                    "response_data": response.json() if response.text else None
                }
                print(f"✅ Passed - Status: {response.status_code}")
            else:
                result = {
                    "name": name,
                    "status": "FAIL",
                    "expected_status": expected_status,
                    "response_code": response.status_code,
                    "response_data": response.json() if response.text else None
                }
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
            
            self.test_results.append(result)
            return status_success, response.json() if response.text else None

        except Exception as e:
            result = {
                "name": name,
                "status": "ERROR",
                "error": str(e)
            }
            self.test_results.append(result)
            print(f"❌ Error - {str(e)}")
            return False, None

    def test_welcome_endpoint(self):
        """Test the welcome endpoint"""
        return self.run_test(
            "Welcome Endpoint",
            "GET",
            "",
            200
        )

    def test_location_analysis(self, city):
        """Test location analysis for a city"""
        return self.run_test(
            f"Location Analysis - {city}",
            "GET",
            f"location-analysis/{city}",
            200
        )

    def test_job_recommendations(self, user_id="user_001"):
        """Test job recommendations for a user"""
        return self.run_test(
            "Job Recommendations",
            "GET",
            f"jobs/recommendations/{user_id}",
            200
        )

    def test_system_status(self):
        """Test system status endpoint"""
        return self.run_test(
            "System Status",
            "GET",
            "system/status",
            200
        )

    def test_bridge_transition_data(self):
        """Test bridge transition data endpoint"""
        return self.run_test(
            "Bridge Transition Data",
            "GET",
            "transition/bridge-data",
            200
        )

    def test_create_location_search(self):
        """Test creating a location search"""
        data = {
            "user_id": "user_001",
            "current_location": "New York",
            "target_cities": ["Austin", "Phoenix", "Peak District"],
            "budget_range": {"min": 2000, "max": 5000},
            "preferences": {"climate": "warm", "cost_of_living": "medium"}
        }
        return self.run_test(
            "Create Location Search",
            "POST",
            "search-locations",
            200,
            data=data
        )

    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "="*50)
        print(f"📊 TEST SUMMARY: {self.tests_passed}/{self.tests_run} tests passed")
        print("="*50)
        
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['name']}: {result['status']}")
        
        print("="*50)
        return self.tests_passed == self.tests_run

def main():
    print("🚀 Starting RelocateMe API Tests")
    print("="*50)
    
    tester = RelocateMeAPITester()
    
    # Test welcome endpoint
    tester.test_welcome_endpoint()
    
    # Test location analysis for different cities
    tester.test_location_analysis("phoenix")
    tester.test_location_analysis("austin")
    tester.test_location_analysis("peak_district")
    
    # Test job recommendations
    tester.test_job_recommendations()
    
    # Test system status
    tester.test_system_status()
    
    # Test bridge transition data
    tester.test_bridge_transition_data()
    
    # Test creating a location search
    tester.test_create_location_search()
    
    # Print summary
    all_passed = tester.print_summary()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    main()
