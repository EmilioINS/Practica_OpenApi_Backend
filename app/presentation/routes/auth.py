from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.domain.entities import LoginRequest, LoginResponse, RegisterRequest, UsuarioResponse
from app.infrastructure.database import get_db
from app.use_cases import auth as auth_use_cases

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Autenticación de usuario"""
    return auth_use_cases.authenticate_user(db, request)

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Registro de nuevo usuario"""
    return auth_use_cases.register_user(db, request)

from app.infrastructure.security import get_current_user_id

@router.get("/me", response_model=UsuarioResponse)
def get_me(db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user_id)):
    """Obtener el perfil del usuario autenticado"""
    return auth_use_cases.get_current_user_profile(db, current_user_id)
