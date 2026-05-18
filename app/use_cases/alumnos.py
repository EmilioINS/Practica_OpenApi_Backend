from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infrastructure.orm_models import AlumnoORM, Usuario
from app.infrastructure.security import get_password_hash
from app.domain.entities import AlumnoInput, Alumno
from typing import List

def get_alumnos(db: Session, page: int = 0, size: int = 10) -> List[Alumno]:
    alumnos_orm = db.query(AlumnoORM).offset(page * size).limit(size).all()
    return [Alumno.model_validate(a) for a in alumnos_orm]

def create_alumno(db: Session, alumno_in: AlumnoInput) -> Alumno:
    # Validate uniqueness
    if db.query(AlumnoORM).filter(AlumnoORM.matricula == alumno_in.matricula).first():
        raise HTTPException(status_code=400, detail="Matrícula ya registrada")
    if db.query(AlumnoORM).filter(AlumnoORM.correo == alumno_in.correo).first():
        raise HTTPException(status_code=400, detail="Correo ya registrado")
        
    usuario = None
    if alumno_in.password:
        if db.query(Usuario).filter(Usuario.username == alumno_in.matricula).first():
            raise HTTPException(status_code=400, detail="Usuario ya existe para esta matrícula")
        usuario = Usuario(
            username=alumno_in.matricula,
            hashed_password=get_password_hash(alumno_in.password)
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        
    alumno = AlumnoORM(
        matricula=alumno_in.matricula,
        nombre=alumno_in.nombre,
        correo=alumno_in.correo,
        id_usuario=usuario.id if usuario else None
    )
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    return Alumno.model_validate(alumno)

from app.domain.entities import AlumnoUpdate

def update_alumno(db: Session, id_alumno: int, alumno_in: AlumnoUpdate) -> Alumno:
    alumno = db.query(AlumnoORM).filter(AlumnoORM.id_alumno == id_alumno).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    if alumno_in.matricula and alumno_in.matricula != alumno.matricula:
        if db.query(AlumnoORM).filter(AlumnoORM.matricula == alumno_in.matricula).first():
            raise HTTPException(status_code=400, detail="Matrícula ya registrada")
        alumno.matricula = alumno_in.matricula
        
    if alumno_in.correo and alumno_in.correo != alumno.correo:
        if db.query(AlumnoORM).filter(AlumnoORM.correo == alumno_in.correo).first():
            raise HTTPException(status_code=400, detail="Correo ya registrado")
        alumno.correo = alumno_in.correo
        
    if alumno_in.nombre:
        alumno.nombre = alumno_in.nombre
        
    if alumno_in.password and alumno.id_usuario:
        usuario = db.query(Usuario).filter(Usuario.id == alumno.id_usuario).first()
        if usuario:
            usuario.hashed_password = get_password_hash(alumno_in.password)

    db.commit()
    db.refresh(alumno)
    return Alumno.model_validate(alumno)

def delete_alumno(db: Session, id_alumno: int):
    alumno = db.query(AlumnoORM).filter(AlumnoORM.id_alumno == id_alumno).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    id_usuario = alumno.id_usuario
    db.delete(alumno)
    
    # Cascade delete user if exists
    if id_usuario:
        usuario = db.query(Usuario).filter(Usuario.id == id_usuario).first()
        if usuario:
            db.delete(usuario)
            
    db.commit()
    return {"message": "Alumno eliminado correctamente"}

def get_available_alumnos(db: Session) -> List[Alumno]:
    alumnos_orm = db.query(AlumnoORM).filter(AlumnoORM.id_equipo == None).all()
    return [Alumno.model_validate(a) for a in alumnos_orm]

def assign_alumno_to_equipo(db: Session, id_alumno: int, id_equipo: int) -> Alumno:
    alumno = db.query(AlumnoORM).filter(AlumnoORM.id_alumno == id_alumno).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    from app.infrastructure.orm_models import EquipoORM
    equipo = db.query(EquipoORM).filter(EquipoORM.id_equipo == id_equipo).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
    alumno.id_equipo = id_equipo
    db.commit()
    db.refresh(alumno)
    return Alumno.model_validate(alumno)

def unassign_alumno(db: Session, id_alumno: int) -> Alumno:
    alumno = db.query(AlumnoORM).filter(AlumnoORM.id_alumno == id_alumno).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
    alumno.id_equipo = None
    db.commit()
    db.refresh(alumno)
    return Alumno.model_validate(alumno)
