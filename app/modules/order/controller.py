from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database import get_db
from app.modules.order.service import OrderService
from app.modules.order.schemas import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_service(db: AsyncSession = Depends(get_db)) -> OrderService:
    return OrderService(db)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate, 
    service: OrderService = Depends(get_service)
):
    return await service.create_order(order_data)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int, 
    service: OrderService = Depends(get_service)
):
    order = await service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    skip: int = 0, 
    limit: int = 100, 
    service: OrderService = Depends(get_service)
):
    return await service.list_orders(skip, limit)

@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int, 
    order_data: OrderUpdate, 
    service: OrderService = Depends(get_service)
):
    order = await service.update_order(order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int, 
    service: OrderService = Depends(get_service)
):
    success = await service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return None
