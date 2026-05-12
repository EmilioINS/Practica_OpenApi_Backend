from sqlalchemy.orm import Session
from app.infrastructure.orm_models import EquipoORM

def get_equipos(db: Session):
    return db.query(EquipoORM).all()
