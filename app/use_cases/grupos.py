from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.infrastructure.orm_models import GrupoORM, MateriaORM
from app.domain.entities import GrupoInput

def create_grupo(db: Session, grupo_in: GrupoInput):
    materia = db.query(MateriaORM).filter(MateriaORM.id_materia == grupo_in.id_materia).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
        
    grupo = GrupoORM(
        nombre_grupo=grupo_in.nombre_grupo,
        id_materia=grupo_in.id_materia
    )
    db.add(grupo)
    db.commit()

def get_grupos(db: Session):
    return db.query(GrupoORM).all()

def get_grupo_by_id(db: Session, id_grupo: int):
    grupo = db.query(GrupoORM).filter(GrupoORM.id_grupo == id_grupo).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo
