from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Date, Text
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)

    piggy_bank = relationship('PiggyBank', uselist=False, back_populates='user')
    goals = relationship('Goal', back_populates='user')
    settings = relationship('Settings', uselist=False, back_populates='user')

    lesson_completions = relationship('UserLessonCompletion', back_populates='user')
    story_completions = relationship('UserStoryCompletion', back_populates='user')

class PiggyBank(Base):
    __tablename__ = 'piggy_banks'

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, default=0.0, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship('User', back_populates='piggy_bank')

class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='goals')

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Add more fields as needed

    completions = relationship('UserLessonCompletion', back_populates='lesson')

class Story(Base):
    __tablename__ = 'stories'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Add more fields for story content here

    completions = relationship('UserStoryCompletion', back_populates='story')

class Tracking(Base):
    __tablename__ = 'tracking'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    money_saved = Column(Float, default=0.0, nullable=False)
    lessons_completed = Column(Integer, default=0, nullable=False)

    user = relationship('User')

class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    notifications_enabled = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=False)
    # Add more preferences here

    user = relationship('User', back_populates='settings')

class UserLessonCompletion(Base):
    __tablename__ = 'user_lesson_completions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='lesson_completions')
    lesson = relationship('Lesson', back_populates='completions')

class UserStoryCompletion(Base):
    __tablename__ = 'user_story_completions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    story_id = Column(Integer, ForeignKey('stories.id'), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='story_completions')
    story = relationship('Story', back_populates='completions')
