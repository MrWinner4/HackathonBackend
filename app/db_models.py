from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date, Text, JSON
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    firebase_uid = Column(String, unique=True, nullable=True, index=True)  # Add this line

    piggy_bank = relationship('PiggyBank', uselist=False, back_populates='user')
    goals = relationship('Goal', back_populates='user')
    settings = relationship('Settings', uselist=False, back_populates='user')

    lesson_completions = relationship('UserLessonCompletion', back_populates='user')
    episode_completions = relationship('UserEpisodeCompletion', back_populates='user')

class PiggyBank(Base):
    __tablename__ = 'piggy_banks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    balance = Column(Float, default=0.0, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship('User', back_populates='piggy_bank')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='goals')

class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    topics = Column(JSON, nullable=False)  # Array of topics
    estimated_read_time = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)

    pages = relationship('EpisodePage', back_populates='episode', cascade='all, delete-orphan')
    completions = relationship('UserEpisodeCompletion', back_populates='episode')

class EpisodePage(Base):
    __tablename__ = 'episode_pages'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    page_id = Column(String, nullable=False)  # Unique page identifier
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    page_type = Column(String, default='content', nullable=False)
    choices = Column(JSON, nullable=True)  # Array of choice objects
    interactive_elements = Column(JSON, nullable=True)  # Array of interactive elements
    episode_id = Column(String, ForeignKey('episodes.id'), nullable=False)

    episode = relationship('Episode', back_populates='pages')

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    learning_objectives = Column(JSON, nullable=False)  # Array of objectives
    topics = Column(JSON, nullable=False)  # Array of topics
    estimated_duration = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)

    pages = relationship('LessonPage', back_populates='lesson', cascade='all, delete-orphan')
    completions = relationship('UserLessonCompletion', back_populates='lesson')

class LessonPage(Base):
    __tablename__ = 'lesson_pages'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    page_id = Column(String, nullable=False)  # Unique page identifier
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    page_type = Column(String, default='content', nullable=False)
    interactive_elements = Column(JSON, nullable=True)  # Array of interactive elements
    lesson_id = Column(String, ForeignKey('lessons.id'), nullable=False)

    lesson = relationship('Lesson', back_populates='pages')

class Tracking(Base):
    __tablename__ = 'tracking'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    money_saved = Column(Float, default=0.0, nullable=False)
    lessons_completed = Column(Integer, default=0, nullable=False)

    user = relationship('User')

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.id'), unique=True, nullable=False)
    notifications_enabled = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=False)
    # Add more preferences here

    user = relationship('User', back_populates='settings')

class UserLessonCompletion(Base):
    __tablename__ = 'user_lesson_completions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(String, ForeignKey('lessons.id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    progress_data = Column(JSON, nullable=True)  # Store quiz answers, choices made, etc.

    user = relationship('User', back_populates='lesson_completions')
    lesson = relationship('Lesson', back_populates='completions')

class UserEpisodeCompletion(Base):
    __tablename__ = 'user_episode_completions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    episode_id = Column(String, ForeignKey('episodes.id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    choices_made = Column(JSON, nullable=True)  # Store the path taken through the story

    user = relationship('User', back_populates='episode_completions')
    episode = relationship('Episode', back_populates='completions')
