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

@router.get("/available", response_model=List[Alumno])
def get_available_alumnos(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Obtener lista de alumnos que no pertenecen a ningún equipo"""
    return alumnos_uc.get_available_alumnos(db)

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

@router.put("/{id_alumno}/assign/{id_equipo}", response_model=Alumno)
def assign_alumno_to_equipo(
    id_alumno: int,
    id_equipo: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Asignar un alumno a un equipo"""
    return alumnos_uc.assign_alumno_to_equipo(db, id_alumno, id_equipo)

@router.delete("/{id_alumno}/unassign", response_model=Alumno)
def unassign_alumno(
    id_alumno: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    """Remover a un alumno de su equipo actual"""
    return alumnos_uc.unassign_alumno(db, id_alumno)
