from datetime import datetime
from pydantic import BaseModel, EmailStr


""" class TypeUser(str, Enum):
    customer = "Customer"
    owner = "Owner"
    agent = "Agent"
    deliverer = "Deliverer"
 """


class TypeUserBase(BaseModel):
    label: str


class TypeUserCreate(TypeUserBase):
    pass


class TypeUserResponse(TypeUserBase):
    id: int

    class Config:
        orm_mode = True


class UsersBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    total_rate: int
    number_rate: int
    rating: int
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    type_user_id: int


class UserResponse(UsersBase):
    type: TypeUserResponse

    class config:
        orm_mode = True
