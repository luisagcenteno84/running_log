from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserSignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPasswordReset(BaseModel):
    email: EmailStr
    new_password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime


class UserSummary(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
