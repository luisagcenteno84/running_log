from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserGoalsUpdate, UserPasswordReset, UserSignIn
from app.security.passwords import hash_password, verify_password


class UserService:
    """Business logic for users."""

    def __init__(self, db):
        self.repo = UserRepository(db)

    def create_user(self, payload: UserCreate) -> User:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')

        user = User(
            id=None,
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )
        return self.repo.create(user)

    def authenticate_user(self, payload: UserSignIn) -> User:
        user = self.repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')
        return user

    def reset_password(self, payload: UserPasswordReset) -> User:
        user = self.repo.get_by_email(payload.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        user.password_hash = hash_password(payload.new_password)
        return self.repo.update(user)

    def update_goals(self, user_id: str, payload: UserGoalsUpdate) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        if payload.goal_weekly_distance_km is not None:
            user.goal_weekly_distance_km = payload.goal_weekly_distance_km
        if payload.goal_avg_pace_seconds is not None:
            user.goal_avg_pace_seconds = payload.goal_avg_pace_seconds
        if payload.goal_training_frequency is not None:
            user.goal_training_frequency = payload.goal_training_frequency

        return self.repo.update(user)

    def list_users(self) -> list[User]:
        return self.repo.list()

    def get_user_or_404(self, user_id: str) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user
