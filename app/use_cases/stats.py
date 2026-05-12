from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.infrastructure.orm_models import ExposicionORM, AlumnoORM, MateriaORM, GrupoORM, EvaluacionDetalleORM, EquipoORM

def get_dashboard_stats(db: Session) -> dict:
    # Contadores básicos
    exposiciones_count = db.query(ExposicionORM).count()
    alumnos_count = db.query(AlumnoORM).count()
    materias_count = db.query(MateriaORM).count()
    grupos_count = db.query(GrupoORM).count()
    
    # Promedio global
    avg_calificacion = db.query(func.avg(EvaluacionDetalleORM.calificacion)).scalar()
    promedio_global = round(avg_calificacion, 1) if avg_calificacion else 0.0

    # Últimas exposiciones
    ultimas = db.query(ExposicionORM).join(EquipoORM).order_by(ExposicionORM.fecha.desc()).limit(5).all()
    ultimas_list = []
    for expo in ultimas:
        ultimas_list.append({
            "fecha": expo.fecha.isoformat() if expo.fecha else None,
            "tema": expo.tema,
            "equipo": expo.equipo.nombre_equipo if expo.equipo else "Sin equipo"
        })

    return {
        "exposiciones": exposiciones_count,
        "alumnos": alumnos_count,
        "materias": materias_count,
        "grupos": grupos_count,
        "promedio": promedio_global,
        "ultimasExposiciones": ultimas_list
    }
