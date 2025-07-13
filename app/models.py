from dataclasses import Field
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class UserRequest(BaseModel):
    username: str
    email: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    piggy_bank: "PiggyBankResponse"
    goals: List["GoalResponse"]
    settings: Optional["SettingsResponse"]


class PiggyBankUpdate(BaseModel):
    balance: float


class PiggyBankResponse(BaseModel):
    balance: float


class GoalRequest(BaseModel):
    name: str
    target_amount: float
    due_date: Optional[date] = None


class GoalResponse(BaseModel):
    id: str
    name: str
    target_amount: float
    due_date: Optional[date] = None
    created_at: datetime


# Add these new models to your models.py file:


class Choice(BaseModel):
    text: str
    next_page: str
    consequence: Optional[str] = None


class InteractiveElement(BaseModel):
    type: str  # 'quiz', 'exercise', etc.
    question: Optional[str] = None
    options: Optional[List[str]] = None
    correct: Optional[int] = None


class Page(BaseModel):
    id: str
    title: str
    content: str
    type: str = "content"  # 'intro', 'content', 'summary'
    choices: Optional[List[Choice]] = None
    interactive_elements: Optional[List[InteractiveElement]] = None


class Episode(BaseModel):
    id: Optional[str] = None
    title: str
    subtitle: str
    emoji: str
    pages: List[Page]
    topics: List[str]
    estimated_read_time: int
    created_at: Optional[datetime] = None


class Lesson(BaseModel):
    id: Optional[str] = None
    title: str
    subtitle: str
    emoji: str
    pages: List[Page]
    learning_objectives: List[str]
    topics: List[str]
    estimated_duration: int
    created_at: Optional[datetime] = None


# Update your existing response models:
class EpisodeResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    emoji: str
    pages: List[Page]
    topics: List[str]
    estimated_read_time: int
    created_at: datetime


class LessonResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    emoji: str
    pages: List[Page]
    learning_objectives: List[str]
    topics: List[str]
    estimated_duration: int
    created_at: datetime


class GenerateContentRequest(BaseModel):
    topic: str
    content_type: str


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
