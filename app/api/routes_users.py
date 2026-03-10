from fastapi import APIRouter, Depends

from app.database.db import get_db
from app.schemas.user_schema import UserCreate, UserGoalsUpdate, UserPasswordReset, UserRead, UserSignIn
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=UserRead, status_code=201)
def create_user(payload: UserCreate, db = Depends(get_db)) -> UserRead:
    user = UserService(db).create_user(payload)
    return UserRead.model_validate(user)


@router.post('/sign-in', response_model=UserRead)
def sign_in(payload: UserSignIn, db = Depends(get_db)) -> UserRead:
    user = UserService(db).authenticate_user(payload)
    return UserRead.model_validate(user)


@router.post('/reset-password', response_model=UserRead)
def reset_password(payload: UserPasswordReset, db = Depends(get_db)) -> UserRead:
    user = UserService(db).reset_password(payload)
    return UserRead.model_validate(user)


@router.put('/{user_id}/goals', response_model=UserRead)
def update_goals(user_id: str, payload: UserGoalsUpdate, db = Depends(get_db)) -> UserRead:
    user = UserService(db).update_goals(user_id, payload)
    return UserRead.model_validate(user)


@router.get('', response_model=list[UserRead])
def list_users(db = Depends(get_db)) -> list[UserRead]:
    users = UserService(db).list_users()
    return [UserRead.model_validate(user) for user in users]
