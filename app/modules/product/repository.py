from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.modules.product.models import Product, Inventory
from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 10):
        # Perform a join to fetch inventory along with product
        stmt = (
            select(Product)
            .options(joinedload(Product.inventory))
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, product_id: str):
        stmt = (
            select(Product)
            .options(joinedload(Product.inventory))
            .where(Product.id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
