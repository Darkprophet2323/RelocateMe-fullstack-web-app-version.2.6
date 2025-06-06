
import requests
import sys
import json
from datetime import datetime

class RelocateMeAPITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def run_test(self, name, method, endpoint, expected_status, data=None, auth_required=False):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        if auth_required and self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)

            success = response.status_code == expected_status
            
            result = {
                "name": name,
                "url": url,
                "method": method,
                "expected_status": expected_status,
                "actual_status": response.status_code,
                "success": success
            }
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                if response.status_code != 204:  # No content
                    try:
                        result["response"] = response.json()
                    except:
                        result["response"] = response.text
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    result["error"] = response.json()
                except:
                    result["error"] = response.text
            
            self.test_results.append(result)
            return success, response.json() if success and response.status_code != 204 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.test_results.append({
                "name": name,
                "url": url,
                "method": method,
                "success": False,
                "error": str(e)
            })
            return False, {}

    def test_login(self, username, password):
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

    def test_login_invalid(self, username, password):
        """Test login with invalid credentials"""
        success, _ = self.run_test(
            "Login with Invalid Credentials",
            "POST",
            "auth/login",
            401,
            data={"username": username, "password": password}
        )
        return success

    def test_password_reset_request(self, username):
        """Test password reset request"""
        success, response = self.run_test(
            "Password Reset Request",
            "POST",
            "auth/reset-password",
            200,
            data={"username": username}
        )
        return success, response.get('reset_code') if success else None

    def test_password_reset_complete(self, username, reset_code, new_password):
        """Test password reset completion"""
        success, _ = self.run_test(
            "Password Reset Completion",
            "POST",
            "auth/complete-password-reset",
            200,
            data={
                "username": username,
                "reset_code": reset_code,
                "new_password": new_password
            }
        )
        return success

    def test_get_user_info(self):
        """Test getting user info"""
        success, _ = self.run_test(
            "Get User Info",
            "GET",
            "auth/me",
            200,
            auth_required=True
        )
        return success

    def test_get_phoenix_data(self):
        """Test getting Phoenix location data"""
        success, _ = self.run_test(
            "Get Phoenix Data",
            "GET",
            "locations/phoenix",
            200
        )
        return success

    def test_get_peak_district_data(self):
        """Test getting Peak District location data"""
        success, _ = self.run_test(
            "Get Peak District Data",
            "GET",
            "locations/peak-district",
            200
        )
        return success

    def test_get_relocation_comparison(self):
        """Test getting relocation comparison data"""
        success, _ = self.run_test(
            "Get Relocation Comparison",
            "GET",
            "comparison/phoenix-to-peak-district",
            200,
            auth_required=True
        )
        return success

    def test_get_phoenix_housing(self):
        """Test getting Phoenix housing data"""
        success, _ = self.run_test(
            "Get Phoenix Housing Data",
            "GET",
            "housing/phoenix",
            200
        )
        return success

    def test_get_peak_district_housing(self):
        """Test getting Peak District housing data"""
        success, _ = self.run_test(
            "Get Peak District Housing Data",
            "GET",
            "housing/peak-district",
            200
        )
        return success

    def test_get_job_opportunities(self):
        """Test getting job opportunities"""
        success, _ = self.run_test(
            "Get Job Opportunities",
            "GET",
            "jobs/opportunities",
            200,
            auth_required=True
        )
        return success
    
    def test_get_job_listings(self, category=None, job_type=None):
        """Test getting job listings with optional filters"""
        endpoint = "jobs/listings"
        if category or job_type:
            params = []
            if category:
                params.append(f"category={category}")
            if job_type:
                params.append(f"job_type={job_type}")
            endpoint += f"?{'&'.join(params)}"
        
        success, response = self.run_test(
            f"Get Job Listings{' (Filtered)' if category or job_type else ''}",
            "GET",
            endpoint,
            200
        )
        return success, response
    
    def test_get_featured_jobs(self):
        """Test getting featured jobs"""
        success, response = self.run_test(
            "Get Featured Jobs",
            "GET",
            "jobs/featured",
            200
        )
        return success, response
    
    def test_get_job_categories(self):
        """Test getting job categories"""
        success, response = self.run_test(
            "Get Job Categories",
            "GET",
            "jobs/categories",
            200
        )
        return success, response
    
    def test_get_visa_requirements(self):
        """Test getting visa requirements"""
        success, response = self.run_test(
            "Get Visa Requirements",
            "GET",
            "visa/requirements",
            200
        )
        return success, response
    
    def test_get_visa_requirement_details(self, visa_type):
        """Test getting specific visa requirement details"""
        success, response = self.run_test(
            f"Get Visa Details for {visa_type}",
            "GET",
            f"visa/requirements/{visa_type}",
            200
        )
        return success, response
    
    def test_get_visa_checklist(self):
        """Test getting visa checklist"""
        success, response = self.run_test(
            "Get Visa Checklist",
            "GET",
            "visa/checklist",
            200
        )
        return success, response

    def test_get_chrome_extensions(self):
        """Test getting Chrome extensions"""
        success, response = self.run_test(
            "Get Chrome Extensions",
            "GET",
            "chrome-extensions",
            200
        )
        return success, response

    def test_download_relocate_helper(self):
        """Test downloading Relocate Helper extension"""
        success, _ = self.run_test(
            "Download Relocate Helper Extension",
            "GET",
            "download/relocate-helper.zip",
            200
        )
        return success

    def test_download_property_finder(self):
        """Test downloading Property Finder extension"""
        success, _ = self.run_test(
            "Download Property Finder Extension",
            "GET",
            "download/property-finder.zip",
            200
        )
        return success

    def test_get_dashboard_overview(self):
        """Test getting dashboard overview"""
        success, _ = self.run_test(
            "Get Dashboard Overview",
            "GET",
            "dashboard/overview",
            200,
            auth_required=True
        )
        return success
    
    def test_get_timeline_full(self):
        """Test getting full timeline"""
        success, response = self.run_test(
            "Get Full Timeline",
            "GET",
            "timeline/full",
            200,
            auth_required=True
        )
        return success, response
    
    def test_get_timeline_by_category(self):
        """Test getting timeline by category"""
        success, response = self.run_test(
            "Get Timeline By Category",
            "GET",
            "timeline/by-category",
            200,
            auth_required=True
        )
        return success, response
    
    def test_get_resources(self):
        """Test getting resources"""
        success, response = self.run_test(
            "Get Resources",
            "GET",
            "resources/all",
            200
        )
        return success, response

    def test_get_progress_items(self, category=None, status=None):
        """Test getting progress items with optional filters"""
        endpoint = "progress/items"
        if category or status:
            params = []
            if category:
                params.append(f"category={category}")
            if status:
                params.append(f"status={status}")
            endpoint += f"?{'&'.join(params)}"
        
        success, response = self.run_test(
            f"Get Progress Items{' (Filtered)' if category or status else ''}",
            "GET",
            endpoint,
            200,
            auth_required=True
        )
        return success, response
    
    def test_toggle_subtask(self, item_id, subtask_index):
        """Test toggling a subtask"""
        success, response = self.run_test(
            f"Toggle Subtask {subtask_index} for Item {item_id}",
            "POST",
            f"progress/items/{item_id}/subtask",
            200,
            data={"subtask_index": subtask_index},
            auth_required=True
        )
        return success, response
    
    def test_update_progress_item(self, item_id, status=None, notes=None, priority=None):
        """Test updating a progress item"""
        data = {}
        if status:
            data["status"] = status
        if notes:
            data["notes"] = notes
        if priority:
            data["priority"] = priority
            
        success, response = self.run_test(
            f"Update Progress Item {item_id}",
            "PUT",
            f"progress/items/{item_id}",
            200,
            data=data,
            auth_required=True
        )
        return success, response
    
    def test_update_timeline_progress(self, step_id, completed, notes=None):
        """Test updating timeline step progress"""
        data = {
            "step_id": step_id,
            "completed": completed
        }
        if notes:
            data["notes"] = notes
            
        success, response = self.run_test(
            f"Update Timeline Step {step_id} Progress",
            "POST",
            "timeline/update-progress",
            200,
            data=data,
            auth_required=True
        )
        return success, response
    
    def test_get_progress_dashboard(self):
        """Test getting progress dashboard"""
        success, response = self.run_test(
            "Get Progress Dashboard",
            "GET",
            "progress/dashboard",
            200,
            auth_required=True
        )
        return success, response
        
    def print_summary(self):
        """Print test summary"""
        
        if self.tests_passed < self.tests_run:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"- {result['name']} ({result['method']} {result['url']})")
                    if "error" in result:
                        print(f"  Error: {result['error']}")
                    print()
        
        return self.tests_passed == self.tests_run

def main():
    # Get the backend URL from the frontend .env file
    backend_url = "https://a0e0ffc6-3b5f-4501-85e6-194acf3953f6.preview.emergentagent.com"
    
    print(f"Testing Relocate Me API at: {backend_url}")
    
    # Setup tester
    tester = RelocateMeAPITester(backend_url)
    
    # Test authentication - critical for noir-themed app testing
    print("\n=== Testing Authentication ===")
    
    # Test login with valid credentials
    if not tester.test_login("relocate_user", "SecurePass2025!"):
        print("❌ Login failed, stopping tests")
        return 1
    else:
        print("✅ Successfully logged in with provided credentials")
    
    # Test user info endpoint to verify user data
    tester.test_get_user_info()
    
    # Test dashboard overview endpoint - important for noir theme verification
    print("\n=== Testing Dashboard Data ===")
    tester.test_get_dashboard_overview()
    
    # Test timeline endpoints - critical for noir theme progress tracking
    print("\n=== Testing Timeline Data ===")
    timeline_success, timeline_data = tester.test_get_timeline_full()
    if timeline_success and 'timeline' in timeline_data:
        print(f"✅ Found {len(timeline_data['timeline'])} timeline steps")
        
        # Test updating a timeline step - verifies interactive noir elements
        if timeline_data['timeline']:
            step = timeline_data['timeline'][0]
            step_id = step['id']
            current_status = step.get('is_completed', False)
            
            # Toggle the step status
            update_success, update_response = tester.test_update_timeline_progress(step_id, not current_status)
            if update_success:
                print(f"✅ Successfully toggled timeline step {step_id} status")
                
                # Toggle it back
                tester.test_update_timeline_progress(step_id, current_status)
    
    # Test progress items endpoints - important for noir checkboxes and progress tracking
    print("\n=== Testing Progress Items ===")
    progress_success, progress_data = tester.test_get_progress_items()
    if progress_success and 'items' in progress_data:
        print(f"✅ Found {len(progress_data['items'])} progress items")
        
        # Test updating a progress item - verifies interactive noir elements
        if progress_data['items']:
            item = progress_data['items'][0]
            item_id = item['id']
            current_status = item.get('status', 'not_started')
            new_status = 'in_progress' if current_status != 'in_progress' else 'completed'
            
            update_success, update_response = tester.test_update_progress_item(item_id, status=new_status)
            if update_success:
                print(f"✅ Successfully updated progress item {item_id} status to {new_status}")
                
                # Test toggling a subtask - verifies interactive noir checkboxes
                if 'subtasks' in item and item['subtasks']:
                    subtask_index = 0
                    toggle_success, toggle_response = tester.test_toggle_subtask(item_id, subtask_index)
                    if toggle_success:
                        print(f"✅ Successfully toggled subtask {subtask_index} for item {item_id}")
    
    # Test progress dashboard - important for noir theme visualization
    tester.test_get_progress_dashboard()
    
    # Test resources endpoint - important for OS Noir link verification
    print("\n=== Testing Resources ===")
    tester.test_get_resources()
    
    # Test job data endpoints - part of noir theme content
    print("\n=== Testing Job Data ===")
    job_listings_success, job_listings = tester.test_get_job_listings()
    if job_listings_success:
        print(f"✅ Found {job_listings.get('total', 0)} job listings")
    
    # Test visa data endpoints - part of noir theme content
    print("\n=== Testing Visa Data ===")
    visa_success, visa_data = tester.test_get_visa_requirements()
    if visa_success and 'visa_types' in visa_data:
        print(f"✅ Found {len(visa_data['visa_types'])} visa types")
    
    # Print summary
    all_passed = tester.print_summary()
    
    print("\n=== Noir Theme API Testing Summary ===")
    print(f"Total tests run: {tester.tests_run}")
    print(f"Tests passed: {tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed / tester.tests_run) * 100:.2f}%")
    
    if all_passed:
        print("\n✅ All backend API tests passed - Backend is ready for noir theme UI testing")
    else:
        print("\n⚠️ Some backend API tests failed - May affect noir theme UI functionality")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
