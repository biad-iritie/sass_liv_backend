from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..models import User
from .. import utils
from .. import oauth2
from .. import database
from ..config import settings
from ..schemas.sch_token import Token
from ..schemas import sch_user


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=Token)
def login_for_access_token(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(User).filter(
        User.email == user_credential.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"},)
    if not utils.verify_password(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"},)
    # CREATE TOKEN
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = oauth2.create_access_token(
        data={"data": user.id}, expire_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/me", response_model=sch_user.UserResponse)
# def get_user_info(current_user: Annotated[sch_user.UserResponse, Depends(oauth2.get_current_user)]):
def get_user_info(current_user: sch_user.UserResponse = Depends(oauth2.get_current_user)):
    return current_user
