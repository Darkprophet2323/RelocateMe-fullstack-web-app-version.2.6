from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="RelocateMe API", version="2.5")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# ============================================================================
# MODELS
# ============================================================================

class LocationSearch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    current_location: str
    target_cities: List[str]
    budget_range: Dict[str, int]  # {"min": 2000, "max": 5000}
    preferences: Dict[str, Any]  # {"climate": "warm", "cost_of_living": "medium"}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LocationSearchCreate(BaseModel):
    user_id: str
    current_location: str
    target_cities: List[str]
    budget_range: Dict[str, int]
    preferences: Dict[str, Any]

class MovingService(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    service_type: str  # "full_service", "self_move", "hybrid"
    from_location: str
    to_location: str
    moving_date: datetime
    estimated_cost: float
    items_count: int
    special_requirements: List[str]
    status: str = "pending"  # "pending", "confirmed", "in_progress", "completed"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MovingServiceCreate(BaseModel):
    user_id: str
    service_type: str
    from_location: str
    to_location: str
    moving_date: datetime
    estimated_cost: float
    items_count: int
    special_requirements: List[str] = []

class UserProfile(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    email: str
    current_location: str
    work_preferences: Dict[str, Any]
    skills: List[str]
    experience_level: str
    remote_work_preference: str  # "fully_remote", "hybrid", "onsite"
    relocation_status: str  # "planning", "in_progress", "completed"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserProfileCreate(BaseModel):
    user_id: str
    name: str
    email: str
    current_location: str
    work_preferences: Dict[str, Any]
    skills: List[str]
    experience_level: str
    remote_work_preference: str
    relocation_status: str = "planning"

class JobOpportunity(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    company: str
    location: str
    remote_friendly: bool
    salary_range: Dict[str, int]
    required_skills: List[str]
    description: str
    application_url: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class LocationAnalysis(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    city: str
    state: str
    country: str
    cost_of_living_index: float
    average_rent: float
    average_salary: float
    climate_score: float
    job_market_score: float
    quality_of_life_score: float
    remote_work_friendliness: float
    pros: List[str]
    cons: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# ============================================================================
# RELOCATION ENDPOINTS
# ============================================================================

@api_router.get("/")
async def root():
    return {"message": "RelocateMe API v2.5 - Your Cinematic Relocation Experience"}

@api_router.post("/search-locations", response_model=LocationSearch)
async def create_location_search(search: LocationSearchCreate):
    search_dict = search.dict()
    search_obj = LocationSearch(**search_dict)
    await db.location_searches.insert_one(search_obj.dict())
    return search_obj

@api_router.get("/search-locations/{user_id}", response_model=List[LocationSearch])
async def get_user_searches(user_id: str):
    searches = await db.location_searches.find({"user_id": user_id}).to_list(100)
    return [LocationSearch(**search) for search in searches]

@api_router.get("/location-analysis/{city}")
async def get_location_analysis(city: str):
    # Sample data - in production this would come from real APIs
    sample_analyses = {
        "phoenix": {
            "city": "Phoenix",
            "state": "Arizona",
            "country": "USA",
            "cost_of_living_index": 103.2,
            "average_rent": 1650,
            "average_salary": 58000,
            "climate_score": 7.5,
            "job_market_score": 8.2,
            "quality_of_life_score": 7.8,
            "remote_work_friendliness": 8.5,
            "pros": ["Low cost of living", "Growing tech scene", "Great weather", "No state income tax"],
            "cons": ["Very hot summers", "Limited public transport", "Water scarcity concerns"]
        },
        "peak_district": {
            "city": "Peak District",
            "state": "Derbyshire",
            "country": "UK",
            "cost_of_living_index": 95.8,
            "average_rent": 1200,
            "average_salary": 45000,
            "climate_score": 6.5,
            "job_market_score": 7.0,
            "quality_of_life_score": 9.2,
            "remote_work_friendliness": 9.0,
            "pros": ["Beautiful countryside", "High quality of life", "Strong remote work culture", "Close to major cities"],
            "cons": ["Limited local job market", "Weather can be unpredictable", "Higher housing costs in desirable areas"]
        },
        "austin": {
            "city": "Austin",
            "state": "Texas", 
            "country": "USA",
            "cost_of_living_index": 108.5,
            "average_rent": 1850,
            "average_salary": 72000,
            "climate_score": 7.8,
            "job_market_score": 9.1,
            "quality_of_life_score": 8.5,
            "remote_work_friendliness": 9.2,
            "pros": ["Thriving tech scene", "No state income tax", "Great food culture", "Music scene"],
            "cons": ["Rising cost of living", "Traffic congestion", "Hot summers"]
        }
    }
    
    city_key = city.lower().replace(" ", "_")
    if city_key in sample_analyses:
        analysis_data = sample_analyses[city_key]
        analysis_obj = LocationAnalysis(**analysis_data)
        return analysis_obj
    else:
        raise HTTPException(status_code=404, detail="Location analysis not found")

@api_router.post("/moving-services", response_model=MovingService)
async def create_moving_service(service: MovingServiceCreate):
    service_dict = service.dict()
    service_obj = MovingService(**service_dict)
    await db.moving_services.insert_one(service_obj.dict())
    return service_obj

@api_router.get("/moving-services/{user_id}", response_model=List[MovingService])
async def get_user_moving_services(user_id: str):
    services = await db.moving_services.find({"user_id": user_id}).to_list(100)
    return [MovingService(**service) for service in services]

# ============================================================================
# THRIVE REMOTE OS ENDPOINTS
# ============================================================================

@api_router.post("/profile", response_model=UserProfile)
async def create_user_profile(profile: UserProfileCreate):
    profile_dict = profile.dict()
    profile_obj = UserProfile(**profile_dict)
    await db.user_profiles.insert_one(profile_obj.dict())
    return profile_obj

@api_router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    profile = await db.user_profiles.find_one({"user_id": user_id})
    if profile:
        return UserProfile(**profile)
    raise HTTPException(status_code=404, detail="User profile not found")

@api_router.put("/profile/{user_id}", response_model=UserProfile)
async def update_user_profile(user_id: str, profile_update: UserProfileCreate):
    profile_dict = profile_update.dict()
    profile_dict["user_id"] = user_id
    profile_obj = UserProfile(**profile_dict)
    
    await db.user_profiles.update_one(
        {"user_id": user_id},
        {"$set": profile_obj.dict()},
        upsert=True
    )
    return profile_obj

@api_router.get("/jobs/recommendations/{user_id}")
async def get_job_recommendations(user_id: str):
    # Sample job opportunities - in production this would match user skills/preferences
    sample_jobs = [
        {
            "title": "Senior Full Stack Developer",
            "company": "TechNova Remote",
            "location": "Remote (Austin, TX Hub)",
            "remote_friendly": True,
            "salary_range": {"min": 95000, "max": 130000},
            "required_skills": ["React", "Node.js", "Python", "AWS"],
            "description": "Join our distributed team building next-gen SaaS platforms.",
            "application_url": "https://technova.com/careers/senior-fullstack"
        },
        {
            "title": "Remote UX Designer",
            "company": "DesignCraft Studios",
            "location": "Remote (Peak District Friendly)",
            "remote_friendly": True,
            "salary_range": {"min": 65000, "max": 85000},
            "required_skills": ["Figma", "User Research", "Prototyping"],
            "description": "Design beautiful, intuitive experiences for global clients.",
            "application_url": "https://designcraft.com/careers/ux-designer"
        },
        {
            "title": "DevOps Engineer",
            "company": "CloudScale Systems",
            "location": "Hybrid (Phoenix Office)",
            "remote_friendly": True,
            "salary_range": {"min": 105000, "max": 140000},
            "required_skills": ["Kubernetes", "Docker", "Terraform", "AWS"],
            "description": "Build and maintain scalable cloud infrastructure.",
            "application_url": "https://cloudscale.com/careers/devops"
        }
    ]
    
    jobs = [JobOpportunity(**job) for job in sample_jobs]
    return {"recommendations": [job.dict() for job in jobs]}

@api_router.get("/system/status")
async def get_system_status():
    return {
        "status": "operational",
        "version": "5.5",
        "services": {
            "relocation_engine": "online",
            "job_matching": "online", 
            "location_analysis": "online",
            "ai_recommendations": "online"
        },
        "uptime": "99.8%",
        "last_updated": datetime.utcnow().isoformat()
    }

@api_router.get("/transition/bridge-data")
async def get_bridge_transition_data():
    return {
        "animation_type": "noir_glitch",
        "duration": 3000,
        "messages": [
            "INITIALIZING RELOCATION MATRIX...",
            "SCANNING REMOTE OPPORTUNITIES...",
            "CONNECTING TO THRIVE OS...",
            "WELCOME TO YOUR NEW LIFE."
        ],
        "redirect_url": "/thrive-os"
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()