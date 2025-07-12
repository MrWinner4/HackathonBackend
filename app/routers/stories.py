from fastapi import APIRouter
from .. import models
from typing import List

router = APIRouter(prefix="/stories", tags=["Stories"])

@router.get("/", response_model=List[models.LessonResponse])
def get_stories():
    # Return all stories (static or from DB)
    return [
        models.StoryResponse(id=1, title="New Shoes"),
        # ...
    ]
