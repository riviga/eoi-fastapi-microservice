from pydantic import BaseModel, Field


class PedidoNuevo(BaseModel):
    quantity: int = Field(..., gt=0, description="Cantidad del fármaco en el pedido", example=42)
    product_id: int = Field(..., description="Identificador del fármaco", example=1)
        

class PedidoAlmacenar(PedidoNuevo):    
    price: float = Field(..., min=0.0, description="Precio del fármaco", example=1.95)     
    fee: float = Field(..., min=0.0, description="Tarifa del pedido", example=1.95)
    total: float = Field(..., min=0.0, description="Precio total del pedido", example=1.95)        
    status: str = Field(..., description="Estado del pedido", example="pending", examples=["pending", "completed", "refunded"])


class PedidoAlmacenado(PedidoAlmacenar):
    id: str = Field(..., description="Identificador del pedido", example="671783895abc5034e397fb21")    