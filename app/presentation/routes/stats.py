<<<<<<< Updated upstream
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.use_cases import stats as stats_use_cases
from app.infrastructure.security import get_current_user_id

router = APIRouter(prefix="/api/v1/stats", tags=["Dashboard Stats"])

@router.get("")
def get_stats(db: Session = Depends(get_db), current_user: str = Depends(get_current_user_id)):
    """Obtiene las estadísticas globales para el dashboard"""
    return stats_use_cases.get_dashboard_stats(db)
=======
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/stats", tags=["Estadisticas"])

@router.get("")
def get_stats():
    """Obtener resumen estadístico para el dashboard"""
    return {
        "exposiciones": 0,
        "alumnos": 0,
        "materias": 0,
        "promedio": 0.0,
        "grupos": 0,
        "ultimasExposiciones": []
    }
>>>>>>> Stashed changes
