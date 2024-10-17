from pydantic import BaseModel, Field

class FarmacoNuevo(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del fármaco", example="Paracetamol")
    tipo: str = Field(..., min_length=3, max_length=50, description="Tipo del fármaco", example="Anti inflamatorio")
    
    class Config:
        from_attributes = True
        

class FarmacoAlmacenado(FarmacoNuevo):
    id: int = Field(..., description="Identificador del fármaco", example="1")