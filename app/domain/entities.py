from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date

# Auth
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    token: str
    expiresIn: int

class RegisterRequest(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Materias
class MateriaBase(BaseModel):
    clave_materia: str
    nombre_materia: str

class Materia(MateriaBase):
    id_materia: int

    class Config:
        from_attributes = True

class PagedMaterias(BaseModel):
    content: List[Materia]
    totalElements: int
    totalPages: int

# Alumnos
class AlumnoBase(BaseModel):
    matricula: str
    nombre: str
    correo: EmailStr

class AlumnoInput(AlumnoBase):
    password: Optional[str] = None # Added for auth

class AlumnoUpdate(BaseModel):
    matricula: Optional[str] = None
    nombre: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None

class Alumno(AlumnoBase):
    id_alumno: int

    class Config:
        from_attributes = True

# Grupos
class GrupoInput(BaseModel):
    nombre_grupo: str
    id_materia: int

class Grupo(GrupoInput):
    id_grupo: int

    class Config:
        from_attributes = True

class AlumnoDetail(AlumnoBase):
    id_alumno: int
    id_equipo: Optional[int] = None

    class Config:
        from_attributes = True

# Equipos
class Equipo(BaseModel):
    id_equipo: int
    nombre_equipo: str
    id_grupo: int

    class Config:
        from_attributes = True

class EquipoDetail(Equipo):
    integrantes: List[AlumnoDetail] = []

    class Config:
        from_attributes = True

class GrupoDetail(Grupo):
    materia: Materia
    equipos: List[EquipoDetail] = []

    class Config:
        from_attributes = True

class AlumnoDetail(AlumnoBase):
    id_alumno: int
    id_equipo: Optional[int] = None

    class Config:
        from_attributes = True



# Equipos
class Equipo(BaseModel):
    id_equipo: int
    nombre_equipo: str
    id_grupo: int

    class Config:
        from_attributes = True

class EquipoDetail(Equipo):
    integrantes: List[AlumnoDetail] = []

    class Config:
        from_attributes = True

class GrupoDetail(Grupo):
    materia: Materia
    equipos: List[EquipoDetail] = []

    class Config:
        from_attributes = True

# Criterios
class CriterioEvaluacion(BaseModel):
    id_criterio: int
    descripcion: str

    class Config:
        from_attributes = True

# Exposiciones
class Exposicion(BaseModel):
    id_exposicion: int
    tema: str
    fecha: date
    id_equipo: int

    class Config:
        from_attributes = True

# Evaluaciones
class EvaluacionDetalleInput(BaseModel):
    id_criterio: int
    calificacion: float = Field(..., ge=0, le=10)

class EvaluacionInput(BaseModel):
    id_exposicion: int
    id_alumno_evaluador: int
    comentarios: str
    detalles: List[EvaluacionDetalleInput]
