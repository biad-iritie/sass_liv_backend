from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError
from ..database import get_db

from .. import models
from ..utils import get_password_hash
from ..schemas import sch_user


router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/type", status_code=status.HTTP_201_CREATED, response_model=sch_user.TypeUserResponse)
def create_type_user(type: sch_user.TypeUserCreate, db: Session = Depends(get_db)):

    new_type = db.query(models.Type_User).filter(
        models.Type_User.label == type.label).first()
    if new_type:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="This type exist already")

    new_type = models.Type_User(**type.dict())
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


@router.get("/type", status_code=status.HTTP_200_OK, response_model=List[sch_user.TypeUserResponse])
def get_type_user(db: Session = Depends(get_db)):
    types = db.query(models.Type_User).all()
    return types


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=sch_user.UserResponse)
def signup(user: sch_user.UserCreate, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if new_user:
        raise HTTPException(status_code=status.HTTP_302_FOUND,
                            detail="Sorry you can't create an account with this email")
    try:
        user.password = get_password_hash(user.password)
        new_user = models.User(**user.dict())
        print(new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except DatabaseError as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Sorry! internal problem, it will be fix soon.")
