from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Annotated
from .config import settings
from .database import get_db
from .models import User
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .schemas.sch_token import TokenData


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    print(SECRET_KEY)
    print(ALGORITHM)
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        # print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        """ print("payload")
        print(token) """
        id = payload.get("data")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError as e:
        print(e)
        raise credentials_exception
    except AssertionError as e:
        print(e)

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate redentials", headers={"WWW-Authenticate": "Bearer"},)
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.id).first()

    return user
