from dataclasses import Field
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class UserRequest(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    piggy_bank: 'PiggyBankResponse'
    goals: List['GoalResponse']
    settings: Optional['SettingsResponse']

class PiggyBankUpdate(BaseModel):
    balance: float
    
class PiggyBankResponse(BaseModel):
    balance: float

class GoalRequest(BaseModel):
    name: str
    target_amount: float
    due_date: Optional[date] = None
    
class GoalResponse(BaseModel):
    id: int
    created_at: datetime

class LessonResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    # add more fields for lesson content and interactivity


class StoryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    # add story content, steps, or choices here

class TrackingResponse(BaseModel):
    date: date
    money_saved: float
    lessons_completed: int


class SettingsResponse(BaseModel):
    notifications_enabled: bool = True
    dark_mode: bool = False
    # add more user preferences here

class UserLessonCompletion(BaseModel):
    user_id: int
    lesson_id: int
    completed_at: datetime

class UserStoryCompletion(BaseModel):
    user_id: int
    story_id: int
    completed_at: datetime