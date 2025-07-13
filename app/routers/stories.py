from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import models
from ..content_generator import generate_story
from ..db import get_db
from ..db_models import Episode as EpisodeDB, EpisodePage as EpisodePageDB
from typing import List
import uuid

router = APIRouter(prefix="/stories", tags=["Stories"])

@router.post("/generate", response_model=models.EpisodeResponse)
async def generate_new_story(request: models.GenerateContentRequest, db: Session = Depends(get_db)):
    """Generate a new interactive story and save it to the database"""
    try:
        story_data = generate_story(request.topic)
        if not story_data:
            raise HTTPException(status_code=500, detail="Failed to generate story")
        
        # Create episode in database
        episode_id = str(uuid.uuid4())
        db_episode = EpisodeDB(
            id=episode_id,
            title=story_data["title"],
            subtitle=story_data["subtitle"],
            emoji=story_data["emoji"],
            topics=story_data["topics"],
            estimated_read_time=story_data["estimated_read_time"],
            is_published=True
        )
        db.add(db_episode)
        
        # Create pages in database
        for page_data in story_data["pages"]:
            db_page = EpisodePageDB(
                page_id=page_data["id"],
                title=page_data["title"],
                content=page_data["content"],
                page_type=page_data.get("type", "content"),
                choices=page_data.get("choices"),
                interactive_elements=page_data.get("interactive_elements"),
                episode_id=episode_id
            )
            db.add(db_page)
        
        db.commit()
        db.refresh(db_episode)
        
        # Convert to response model
        episode = models.Episode(
            id=episode_id,
            title=story_data["title"],
            subtitle=story_data["subtitle"],
            emoji=story_data["emoji"],
            pages=[models.Page(**page) for page in story_data["pages"]],
            topics=story_data["topics"],
            estimated_read_time=story_data["estimated_read_time"],
            created_at=db_episode.created_at
        )
        
        return episode
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")

@router.get("/", response_model=List[models.EpisodeResponse])
def get_episodes(db: Session = Depends(get_db)):
    """Get all published episodes"""
    db_episodes = db.query(EpisodeDB).filter(EpisodeDB.is_published == True).all()
    
    episodes = []
    for db_episode in db_episodes:
        # Get pages for this episode
        db_pages = db.query(EpisodePageDB).filter(EpisodePageDB.episode_id == db_episode.id).all()
        
        # Convert pages to models
        pages = []
        for db_page in db_pages:
            page = models.Page(
                id=db_page.page_id,
                title=db_page.title,
                content=db_page.content,
                type=db_page.page_type,
                choices=db_page.choices,
                interactive_elements=db_page.interactive_elements
            )
            pages.append(page)
        
        # Create episode response
        episode = models.Episode(
            id=str(db_episode.id),
            title=db_episode.title,
            subtitle=db_episode.subtitle,
            emoji=db_episode.emoji,
            pages=pages,
            topics=db_episode.topics,
            estimated_read_time=db_episode.estimated_read_time,
            created_at=db_episode.created_at
        )
        episodes.append(episode)
    
    return episodes

@router.get("/{episode_id}", response_model=models.EpisodeResponse)
def get_episode(episode_id: str, db: Session = Depends(get_db)):
    """Get a specific episode by ID"""
    db_episode = db.query(EpisodeDB).filter(EpisodeDB.id == episode_id).first()
    if not db_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    # Get pages for this episode
    db_pages = db.query(EpisodePageDB).filter(EpisodePageDB.episode_id == episode_id).all()
    
    # Convert pages to models
    pages = []
    for db_page in db_pages:
        page = models.Page(
            id=db_page.page_id,
            title=db_page.title,
            content=db_page.content,
            type=db_page.page_type,
            choices=db_page.choices,
            interactive_elements=db_page.interactive_elements
        )
        pages.append(page)
    
    # Create episode response
    episode = models.Episode(
        id=str(db_episode.id),
        title=db_episode.title,
        subtitle=db_episode.subtitle,
        emoji=db_episode.emoji,
        pages=pages,
        topics=db_episode.topics,
        estimated_read_time=db_episode.estimated_read_time,
        created_at=db_episode.created_at
    )
    
    return episode