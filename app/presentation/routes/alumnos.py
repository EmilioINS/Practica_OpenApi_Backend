from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app.infrastructure.database import get_db
from app.infrastructure.security import get_current_user_id
from app.domain.entities import AlumnoInput, Alumno
from app.use_cases import alumnos as alumnos_uc

router = APIRouter(prefix="/api/v1/alumnos", tags=["Alumnos"])

@router.get("", response_model=Dict[str, List[Alumno]])
def get_alumnos(
    page: int = Query(0),
    size: int = Query(10),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Obtener lista de alumnos"""
    content = alumnos_uc.get_alumnos(db, page, size)
    return {"content": content}

@router.post("", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(
    alumno: AlumnoInput,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Registrar un nuevo alumno"""
    return alumnos_uc.create_alumno(db, alumno)

from app.domain.entities import AlumnoUpdate

@router.put("/{id_alumno}", response_model=Alumno)
def update_alumno(
    id_alumno: int,
    alumno: AlumnoUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Actualizar datos de un alumno"""
    return alumnos_uc.update_alumno(db, id_alumno, alumno)

@router.delete("/{id_alumno}")
def delete_alumno(
    id_alumno: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Eliminar un alumno"""
    return alumnos_uc.delete_alumno(db, id_alumno)
