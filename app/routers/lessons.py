from fastapi import APIRouter
from .. import models
from typing import List

router = APIRouter(prefix="/lessons", tags=["Lessons"])

@router.get("/", response_model=List[models.LessonResponse])
def get_lessons():
    # Return all lessons (static or from DB)
    return [
        models.LessonResponse(id=1, title="Saving Basics"),
        # ...
    ]
