from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import db_models, models
from typing import List

router = APIRouter(prefix="/goals", tags=["Goals"])

def get_current_user(db: Session = Depends(get_db)):
    # TODO: Replace with Firebase token verification
    return db.query(db_models.User).first()

@router.get("/", response_model=List[models.GoalRequest])
def get_goals(user=Depends(get_current_user)):
    return user.goals

@router.post("/", response_model=models.GoalRequest)
def add_goal(goal: models.GoalRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_goal = db_models.Goal(**goal.dict(), user_id=user.id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.put("/{goal_id}", response_model=models.GoalRequest)
def update_goal(goal_id: int, goal: models.GoalRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_goal = db.query(db_models.Goal).filter_by(id=goal_id, user_id=user.id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    for key, value in goal.dict().items():
        setattr(db_goal, key, value)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.delete("/{goal_id}")
def delete_goal(goal_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_goal = db.query(db_models.Goal).filter_by(id=goal_id, user_id=user.id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db.delete(db_goal)
    db.commit()
    return {"status": "deleted"}
