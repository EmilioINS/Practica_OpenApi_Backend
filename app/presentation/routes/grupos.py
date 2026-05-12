from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.security import get_current_user_id
from app.domain.entities import GrupoInput
from app.use_cases import grupos as grupos_uc

router = APIRouter(prefix="/api/v1/grupos", tags=["Grupos"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_grupo(
    grupo: GrupoInput,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Crear un nuevo grupo escolar"""
    grupos_uc.create_grupo(db, grupo)
    return {"message": "Grupo creado exitosamente"}

from typing import List
from app.domain.entities import Grupo

@router.get("", response_model=List[Grupo])
def get_grupos(db: Session = Depends(get_db)):
    """Obtener lista de todos los grupos"""
    return grupos_uc.get_grupos(db)
