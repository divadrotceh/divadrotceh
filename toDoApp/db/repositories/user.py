from sqlalchemy.orm import Session
from app.db.models.user import User

def update_user(
    db: Session,
    user_id: int,
    *,
    email: str | None = None,
    password_hash: str | None = None,
):
    user = db.get(User, user_id)
    if not user:
        return None

    if email is not None:
        user.email = email

    if password_hash is not None:
        user.password_hash = password_hash

    db.commit()
    db.refresh(user)
    return user
