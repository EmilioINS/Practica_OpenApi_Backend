from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.domain.entities import Equipo
from app.use_cases import equipos as equipos_uc

router = APIRouter(prefix="/api/v1/equipos", tags=["Equipos"])

@router.get("", response_model=List[Equipo])
def get_equipos(db: Session = Depends(get_db)):
    """Obtener lista de todos los equipos"""
    return equipos_uc.get_equipos(db)
