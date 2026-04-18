from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_token

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "user created"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": db_user.username,
        "user_id": db_user.id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }