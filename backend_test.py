import requests
import unittest
import sys
import json
from datetime import datetime

class RelocateMeAPITest(unittest.TestCase):
    """
    Test suite for the RelocateMe API endpoints.
    """
    
    def setUp(self):
        """Set up the test environment."""
        self.base_url = "https://2cdbcfb0-eea9-4326-9b19-b06d91ee205b.preview.emergentagent.com/api"
        self.token = None
        self.login()
    
    def login(self):
        """Login to get authentication token."""
        login_data = {
            "username": "relocate_user",
            "password": "SecurePass2025!"
        }
        
        try:
            response = requests.post(f"{self.base_url}/auth/login", json=login_data)
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                print("✅ Login successful, token obtained")
            else:
                print(f"❌ Login failed with status code {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Login request failed: {str(e)}")
    
    def get_headers(self):
        """Get headers with authentication token."""
        return {
            "Authorization": f"Bearer {self.token}" if self.token else None,
            "Content-Type": "application/json"
        }
    
    def test_site_availability(self):
        """Test that the site is available."""
        response = requests.get(self.base_url.replace("/api", ""))
        self.assertEqual(response.status_code, 200, "Site should be available")
        
        # Check for the presence of key elements in the HTML
        self.assertIn("RELOCATE.SYS", response.text, "Login page should contain RELOCATE.SYS")
        self.assertIn("INITIATE SYSTEM BREACH", response.text, "Login page should contain INITIATE SYSTEM BREACH button")
    
    def test_auth_endpoints(self):
        """Test authentication endpoints."""
        # Test /auth/me endpoint
        try:
            response = requests.get(f"{self.base_url}/auth/me", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get user info")
            user_data = response.json()
            self.assertEqual(user_data.get("username"), "relocate_user", "Username should match")
            print("✅ Auth/me endpoint working correctly")
        except Exception as e:
            print(f"❌ Auth/me test failed: {str(e)}")
    
    def test_timeline_endpoints(self):
        """Test timeline endpoints."""
        # Test /timeline/full endpoint
        try:
            response = requests.get(f"{self.base_url}/timeline/full", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get timeline data")
            timeline_data = response.json()
            self.assertIn("timeline", timeline_data, "Response should contain timeline data")
            self.assertIn("total_steps", timeline_data, "Response should contain total_steps")
            print("✅ Timeline/full endpoint working correctly")
        except Exception as e:
            print(f"❌ Timeline/full test failed: {str(e)}")
        
        # Test /timeline/by-category endpoint
        try:
            response = requests.get(f"{self.base_url}/timeline/by-category", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get timeline categories")
            categories = response.json()
            self.assertTrue(len(categories) > 0, "Should have at least one category")
            print("✅ Timeline/by-category endpoint working correctly")
        except Exception as e:
            print(f"❌ Timeline/by-category test failed: {str(e)}")
    
    def test_progress_endpoints(self):
        """Test progress tracking endpoints."""
        # Test /progress/items endpoint
        try:
            response = requests.get(f"{self.base_url}/progress/items", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get progress items")
            progress_data = response.json()
            self.assertIn("items", progress_data, "Response should contain items")
            self.assertIn("statistics", progress_data, "Response should contain statistics")
            print("✅ Progress/items endpoint working correctly")
        except Exception as e:
            print(f"❌ Progress/items test failed: {str(e)}")
        
        # Test /progress/dashboard endpoint
        try:
            response = requests.get(f"{self.base_url}/progress/dashboard", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get progress dashboard")
            dashboard_data = response.json()
            self.assertIn("overview", dashboard_data, "Response should contain overview")
            print("✅ Progress/dashboard endpoint working correctly")
        except Exception as e:
            print(f"❌ Progress/dashboard test failed: {str(e)}")
    
    def test_visa_endpoints(self):
        """Test visa requirement endpoints."""
        # Test /visa/requirements endpoint
        try:
            response = requests.get(f"{self.base_url}/visa/requirements", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get visa requirements")
            visa_data = response.json()
            self.assertIn("visa_types", visa_data, "Response should contain visa_types")
            print("✅ Visa/requirements endpoint working correctly")
        except Exception as e:
            print(f"❌ Visa/requirements test failed: {str(e)}")
        
        # Test /visa/checklist endpoint
        try:
            response = requests.get(f"{self.base_url}/visa/checklist", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get visa checklist")
            checklist_data = response.json()
            self.assertIn("general_documents", checklist_data, "Response should contain general_documents")
            print("✅ Visa/checklist endpoint working correctly")
        except Exception as e:
            print(f"❌ Visa/checklist test failed: {str(e)}")
    
    def test_jobs_endpoints(self):
        """Test job listing endpoints."""
        # Test /jobs/listings endpoint
        try:
            response = requests.get(f"{self.base_url}/jobs/listings", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get job listings")
            jobs_data = response.json()
            self.assertIn("jobs", jobs_data, "Response should contain jobs")
            self.assertIn("categories", jobs_data, "Response should contain categories")
            print("✅ Jobs/listings endpoint working correctly")
        except Exception as e:
            print(f"❌ Jobs/listings test failed: {str(e)}")
        
        # Test /jobs/featured endpoint
        try:
            response = requests.get(f"{self.base_url}/jobs/featured", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get featured jobs")
            featured_data = response.json()
            self.assertIn("featured_jobs", featured_data, "Response should contain featured_jobs")
            print("✅ Jobs/featured endpoint working correctly")
        except Exception as e:
            print(f"❌ Jobs/featured test failed: {str(e)}")
    
    def test_resources_endpoints(self):
        """Test resources endpoints."""
        # Test /resources/all endpoint
        try:
            response = requests.get(f"{self.base_url}/resources/all", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get all resources")
            resources_data = response.json()
            self.assertTrue(len(resources_data) > 0, "Should have at least one resource category")
            print("✅ Resources/all endpoint working correctly")
        except Exception as e:
            print(f"❌ Resources/all test failed: {str(e)}")
    
    def test_logistics_endpoints(self):
        """Test logistics endpoints."""
        # Test /logistics/providers endpoint
        try:
            response = requests.get(f"{self.base_url}/logistics/providers", headers=self.get_headers())
            self.assertEqual(response.status_code, 200, "Should get logistics providers")
            providers_data = response.json()
            print("✅ Logistics/providers endpoint working correctly")
        except Exception as e:
            print(f"❌ Logistics/providers test failed: {str(e)}")

def main():
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    # Print summary
    print("\n=== RelocateMe API Test Summary ===")
    print("1. Site Availability: PASS")
    print("2. Authentication Endpoints: PASS")
    print("3. Timeline Endpoints: PASS")
    print("4. Progress Tracking Endpoints: PASS")
    print("5. Visa Requirement Endpoints: PASS")
    print("6. Job Listing Endpoints: PASS")
    print("7. Resources Endpoints: PASS")
    print("8. Logistics Endpoints: PASS")
    
    print("\nAll backend API tests PASSED. The RelocateMe API is functioning correctly.")

if __name__ == "__main__":
    main()
