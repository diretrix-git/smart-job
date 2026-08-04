from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserOut, Token, UserUpdate

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
):
    """
    Create new user.
    """
    user_by_email = crud_user.get_user_by_email(db, email=user_in.email)
    if user_by_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user_by_username = crud_user.get_user_by_username(db, username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud_user.create_user(db, user_in=user_in)
    return user


@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserOut)
def read_user_me(
    current_user = Depends(deps.get_current_user),
):
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserOut)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user = Depends(deps.get_current_user),
):
    """
    Update own user.
    """
    if user_in.username:
        user_by_username = crud_user.get_user_by_username(db, username=user_in.username)
        if user_by_username and user_by_username.id != current_user.id:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
    user = crud_user.update_user(db, db_user=current_user, user_in=user_in)
    return user
