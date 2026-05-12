from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.domain.entities import LoginRequest, LoginResponse, RegisterRequest, UsuarioResponse
from app.infrastructure.orm_models import Usuario
from app.infrastructure.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from datetime import timedelta

def authenticate_user(db: Session, request: LoginRequest) -> LoginResponse:
    user = db.query(Usuario).filter(Usuario.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return LoginResponse(
        token=access_token,
        expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

def register_user(db: Session, request: RegisterRequest) -> UsuarioResponse:
    existing_user = db.query(Usuario).filter(Usuario.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado",
        )
    
    new_user = Usuario(
        username=request.username,
        hashed_password=get_password_hash(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UsuarioResponse.model_validate(new_user)

def get_current_user_profile(db: Session, user_id: str) -> UsuarioResponse:
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return UsuarioResponse.model_validate(user)
