from pydantic import BaseModel, Field

class FarmacoNuevo(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre del fármaco", example="Paracetamol")
    price: float = Field(..., min=0.0, description="Precio del fármaco", example=1.95)
    quantity: int = Field(..., min=0, description="Cantidad del fármaco en inventario", example=42)
    
    class Config:
        from_attributes = True
        

class FarmacoAlmacenado(FarmacoNuevo):
    id: int = Field(..., description="Identificador del fármaco", example="1")