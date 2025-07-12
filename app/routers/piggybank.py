from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, db_models
from ..db import get_db

router = APIRouter()

@router.put("/users/{user_id}/piggy_bank", response_model=models.PiggyBankUpdate)
def update_piggy_bank_balance(user_id: int, update: models.PiggyBankUpdate, db: Session = Depends(get_db)):
    piggy_bank = db.query(db_models.PiggyBank).filter(db_models.PiggyBank.user_id == user_id).first()
    if not piggy_bank:
        piggy_bank = db_models.PiggyBank(user_id=user_id, balance=update.balance)
        db.add(piggy_bank)
    else:
        piggy_bank.balance = update.balance

    db.commit()
    db.refresh(piggy_bank)
    return {"balance": piggy_bank.balance}

def create_piggy_bank(user_id: int, update: models.PiggyBankUpdate, db: Session = Depends(get_db)):
    piggy_bank = db_models.PiggyBank(user_id=user_id, balance=update.balance)
    db.add(piggy_bank)
    db.commit()
    db.refresh(piggy_bank)
    return {"balance": piggy_bank.balance}