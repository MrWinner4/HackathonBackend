from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from firebase_admin import auth as firebase_auth
from app.models import UserRequest, UserResponse
from .. import models, db_models
from ..db import get_db
from .piggybank import create_piggy_bank

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user(db: Session = Depends(get_db)):
    # TODO: Replace with Firebase token verification
    user = db.query(db_models.User).first()  # Placeholder: get first user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=models.UserResponse)
def get_me(user=Depends(get_current_user)):
    # Serialize user and related data
    return models.UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        piggy_bank=models.PiggyBankResponse(balance=user.piggy_bank.balance if user.piggy_bank else 0.0),
        goals=[models.GoalResponse(
            id=goal.id,
            name=goal.name,
            target_amount=goal.target_amount,
            due_date=goal.due_date,
            created_at=goal.created_at
        ) for goal in user.goals],
        settings=models.SettingsResponse(
            notifications_enabled=user.settings.notifications_enabled if user.settings else True,
            dark_mode=user.settings.dark_mode if user.settings else False
        ) if user.settings else None,
    )


@router.post("/register", response_model=UserResponse)
def register_user(request: Request, user: UserRequest, db: Session = Depends(get_db)):
    # 1. Get the Firebase ID token from the Authorization header
    id_token = request.headers.get('Authorization')
    if not id_token:
        raise HTTPException(status_code=401, detail='Missing Firebase ID token')
    
    try:
        # 2. Verify the token with Firebase Admin SDK
        decoded_token = firebase_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email') or user.email
        
        # 3. Check if user already exists
        existing_user = db.query(db_models.User).filter_by(firebase_uid=uid).first()
        if existing_user:
            raise HTTPException(status_code=409, detail='User already exists')
        
        # 4. Create user with Firebase UID
        user_obj = db_models.User(firebase_uid=uid, username=user.username, email=email)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        
        # 5. Create piggy bank
        piggy_bank = db_models.PiggyBank(
            user_id=user_obj.id,
            balance=00.00  # Start with some money
        )
        db.add(piggy_bank)
        db.commit()
        
        # 7. Return clean, serialized user object
        return models.UserResponse(
            id=user_obj.id,
            username=user_obj.username,
            email=user_obj.email,
            piggy_bank=models.PiggyBankResponse(balance=piggy_bank.balance),
            goals=[],  # No goals - user will create their own
            settings=None,
        )
        
    except Exception as e:
        print(f"Firebase token verification failed: {e}")
        raise HTTPException(status_code=401, detail=f'Invalid Firebase ID token: {str(e)}')
