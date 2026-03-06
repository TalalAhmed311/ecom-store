from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database import get_db
from app.modules.product.service import ProductService
from app.modules.product.repository import ProductRepository
from app.modules.product.schemas import ProductResponse
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

def get_product_service(session: AsyncSession = Depends(get_db)) -> ProductService:
    repository = ProductRepository(session)
    return ProductService(repository)

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0, 
    limit: int = 10, 
    service: ProductService = Depends(get_product_service)
):
    return await service.get_products(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str, 
    service: ProductService = Depends(get_product_service)
):
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
