"""
Data models and types for the pet booking system
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

class BookingStep(Enum):
    """Enumeration of booking flow steps"""
    DISCOVERY = "discovery"
    SELECTION = "selection"
    SCHEDULING = "scheduling"
    PET_INFO = "pet_info"
    REVIEW = "review"
    SUCCESS = "success"
    MANAGEMENT = "management"

@dataclass
class Service:
    """Service data model"""
    id: str
    title: str
    description: str
    price: float
    duration: str
    image: str
    features: List[str] = field(default_factory=list)
    popular: bool = False

@dataclass
class BookingData:
    """Main booking data container"""
    service: Optional[Service] = None
    date: Optional[str] = None
    time: Optional[str] = None
    pet_name: Optional[str] = None
    pet_type: Optional[str] = None
    pet_age: Optional[int] = None
    pet_weight: Optional[str] = None
    notes: Optional[str] = None
    booking_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def update(self, data: Dict[str, Any]):
        """Update booking data with new values"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'service': self.service.__dict__ if self.service else None,
            'date': self.date,
            'time': self.time,
            'pet_name': self.pet_name,
            'pet_type': self.pet_type,
            'pet_age': self.pet_age,
            'pet_weight': self.pet_weight,
            'notes': self.notes,
            'booking_id': self.booking_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def is_complete(self) -> bool:
        """Check if all required booking data is present"""
        return all([
            self.service,
            self.date,
            self.time,
            self.pet_name,
            self.pet_type
        ])

# Sample services data
SAMPLE_SERVICES = [
    Service(
        id="grooming-basic",
        title="Basic Grooming",
        description="Essential grooming services including bath, brush, nail trim, and ear cleaning",
        price=45.00,
        duration="1-2 hours",
        image="/placeholder.svg?height=200&width=300",
        features=["Bath & Dry", "Brush & Detangle", "Nail Trim", "Ear Cleaning"]
    ),
    Service(
        id="grooming-premium",
        title="Premium Grooming",
        description="Complete grooming package with styling, teeth cleaning, and premium products",
        price=85.00,
        duration="2-3 hours",
        image="/placeholder.svg?height=200&width=300",
        features=["Everything in Basic", "Professional Styling", "Teeth Cleaning", "Premium Products", "Nail Polish"],
        popular=True
    ),
    Service(
        id="veterinary-checkup",
        title="Veterinary Checkup",
        description="Comprehensive health examination by licensed veterinarians",
        price=75.00,
        duration="30-45 minutes",
        image="/placeholder.svg?height=200&width=300",
        features=["Physical Examination", "Vaccination Check", "Health Report", "Treatment Recommendations"]
    ),
    Service(
        id="pet-sitting",
        title="Pet Sitting",
        description="Professional in-home pet care while you're away",
        price=35.00,
        duration="Per day",
        image="/placeholder.svg?height=200&width=300",
        features=["Daily Visits", "Feeding & Water", "Exercise & Play", "Photo Updates"]
    ),
    Service(
        id="dog-walking",
        title="Dog Walking",
        description="Daily exercise and socialization for your furry friend",
        price=25.00,
        duration="30-60 minutes",
        image="/placeholder.svg?height=200&width=300",
        features=["Individual Walks", "Exercise & Play", "Socialization", "GPS Tracking"]
    ),
    Service(
        id="pet-training",
        title="Pet Training",
        description="Professional behavioral training and obedience classes",
        price=60.00,
        duration="1 hour",
        image="/placeholder.svg?height=200&width=300",
        features=["Behavioral Assessment", "Custom Training Plan", "Progress Tracking", "Owner Education"]
    )
]

# Pet types for dropdown
PET_TYPES = [
    "Dog", "Cat", "Bird", "Rabbit", "Hamster", "Guinea Pig", 
    "Fish", "Reptile", "Ferret", "Other"
]

# Weight categories
WEIGHT_CATEGORIES = [
    "Under 10 lbs", "10-25 lbs", "25-50 lbs", 
    "50-75 lbs", "75-100 lbs", "Over 100 lbs"
]
