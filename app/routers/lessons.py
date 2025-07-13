from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models, db_models
from ..content_generator import generate_lesson
from ..db import get_db
from ..db_models import Lesson as LessonDB, LessonPage as LessonPageDB
from typing import List
import uuid

router = APIRouter(prefix="/lessons", tags=["Lessons"])

def get_current_user(db: Session = Depends(get_db)):
    # TODO: Replace with Firebase token verification
    return db.query(db_models.User).first()

@router.post("/generate", response_model=models.LessonResponse)
async def generate_new_lesson(request: models.GenerateContentRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate a new educational lesson and save it to the database"""
    try:
        lesson_data = generate_lesson(request.topic)
        if not lesson_data:
            raise HTTPException(status_code=500, detail="Failed to generate lesson")
        
        # Create lesson in database
        lesson_id = str(uuid.uuid4())
        db_lesson = LessonDB(
            id=lesson_id,
            title=lesson_data["title"],
            subtitle=lesson_data["subtitle"],
            emoji=lesson_data["emoji"],
            learning_objectives=lesson_data["learning_objectives"],
            topics=lesson_data["topics"],
            estimated_duration=lesson_data["estimated_duration"],
            is_published=True,
            user_id=current_user.id,
        )
        db.add(db_lesson)
        
        # Create pages in database
        for page_data in lesson_data["pages"]:
            db_page = LessonPageDB(
                page_id=page_data["id"],
                title=page_data["title"],
                content=page_data["content"],
                page_type=page_data.get("type", "content"),
                interactive_elements=page_data.get("interactive_elements"),
                lesson_id=lesson_id
            )
            db.add(db_page)
        
        db.commit()
        db.refresh(db_lesson)
        
        # Convert to response model
        lesson = models.Lesson(
            id=lesson_id,
            title=lesson_data["title"],
            subtitle=lesson_data["subtitle"],
            emoji=lesson_data["emoji"],
            pages=[models.Page(**page) for page in lesson_data["pages"]],
            learning_objectives=lesson_data["learning_objectives"],
            topics=lesson_data["topics"],
            estimated_duration=lesson_data["estimated_duration"],
            created_at=db_lesson.created_at
        )
        
        return lesson
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating lesson: {str(e)}")

@router.get("/", response_model=List[models.LessonResponse])
def get_lessons(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all published lessons for the current user"""
    db_lessons = db.query(LessonDB).filter(
        LessonDB.is_published == True,
        LessonDB.user_id == current_user.id
    ).all()
    
    lessons = []
    for db_lesson in db_lessons:
        # Get pages for this lesson
        db_pages = db.query(LessonPageDB).filter(LessonPageDB.lesson_id == db_lesson.id).all()
        
        # Convert pages to models
        pages = []
        for db_page in db_pages:
            page = models.Page(
                id=db_page.page_id,
                title=db_page.title,
                content=db_page.content,
                type=db_page.page_type,
                interactive_elements=db_page.interactive_elements
            )
            pages.append(page)
        
        # Create lesson response
        lesson = models.Lesson(
            id=str(db_lesson.id),
            title=db_lesson.title,
            subtitle=db_lesson.subtitle,
            emoji=db_lesson.emoji,
            pages=pages,
            learning_objectives=db_lesson.learning_objectives,
            topics=db_lesson.topics,
            estimated_duration=db_lesson.estimated_duration,
            created_at=db_lesson.created_at
        )
        lessons.append(lesson)
    
    return lessons

@router.get("/{lesson_id}", response_model=models.LessonResponse)
def get_lesson(lesson_id: str, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    """Get a specific lesson by ID for the current user"""
    db_lesson = db.query(LessonDB).filter(
        LessonDB.id == lesson_id,
        LessonDB.user_id == current_user.id
    ).first()
    if not db_lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    # Get pages for this lesson
    db_pages = db.query(LessonPageDB).filter(LessonPageDB.lesson_id == lesson_id).all()
    
    # Convert pages to models
    pages = []
    for db_page in db_pages:
        page = models.Page(
            id=db_page.page_id,
            title=db_page.title,
            content=db_page.content,
            type=db_page.page_type,
            interactive_elements=db_page.interactive_elements
        )
        pages.append(page)
    
    # Create lesson response
    lesson = models.Lesson(
        id=str(db_lesson.id),
        title=db_lesson.title,
        subtitle=db_lesson.subtitle,
        emoji=db_lesson.emoji,
        pages=pages,
        learning_objectives=db_lesson.learning_objectives,
        topics=db_lesson.topics,
        estimated_duration=db_lesson.estimated_duration,
        created_at=db_lesson.created_at
    )
    
    return lesson
