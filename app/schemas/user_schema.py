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


class UserGoalsUpdate(BaseModel):
    goal_weekly_distance_km: float | None = Field(default=None, ge=0)
    goal_avg_pace_seconds: float | None = Field(default=None, gt=0)
    goal_training_frequency: int | None = Field(default=None, ge=0)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    goal_weekly_distance_km: float | None = None
    goal_avg_pace_seconds: float | None = None
    goal_training_frequency: int | None = None


class UserSummary(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
