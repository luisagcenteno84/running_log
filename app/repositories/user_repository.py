from __future__ import annotations

from datetime import datetime, timezone

from app.models.user import User


class UserRepository:
    """Persistence operations for users backed by Firestore."""

    def __init__(self, db):
        self.db = db
        self.collection = db.collection('users')

    def _to_model(self, document) -> User | None:
        if not document.exists:
            return None
        payload = document.to_dict() or {}
        return User(
            id=document.id,
            name=payload['name'],
            email=payload['email'],
            password_hash=payload.get('password_hash'),
            goal_weekly_distance_km=payload.get('goal_weekly_distance_km'),
            goal_avg_pace_seconds=payload.get('goal_avg_pace_seconds'),
            goal_training_frequency=payload.get('goal_training_frequency'),
            created_at=payload.get('created_at'),
        )

    def _serialize(self, user: User) -> dict:
        return {
            'name': user.name,
            'email': user.email,
            'password_hash': user.password_hash,
            'goal_weekly_distance_km': user.goal_weekly_distance_km,
            'goal_avg_pace_seconds': user.goal_avg_pace_seconds,
            'goal_training_frequency': user.goal_training_frequency,
            'created_at': user.created_at or datetime.now(timezone.utc),
        }

    def create(self, user: User) -> User:
        doc_ref = self.collection.document()
        user.id = doc_ref.id
        user.created_at = user.created_at or datetime.now(timezone.utc)
        doc_ref.set(self._serialize(user))
        return user

    def update(self, user: User) -> User:
        if not user.id:
            raise ValueError('User ID is required for update')
        user.created_at = user.created_at or datetime.now(timezone.utc)
        self.collection.document(user.id).set(self._serialize(user))
        return user

    def list(self) -> list[User]:
        users = [self._to_model(doc) for doc in self.collection.stream()]
        materialized = [user for user in users if user is not None]
        return sorted(materialized, key=lambda user: (user.created_at or datetime.min.replace(tzinfo=timezone.utc)), reverse=True)

    def get_by_id(self, user_id: str) -> User | None:
        return self._to_model(self.collection.document(user_id).get())

    def get_by_email(self, email: str) -> User | None:
        for user in self.list():
            if user.email.lower() == email.lower():
                return user
        return None
