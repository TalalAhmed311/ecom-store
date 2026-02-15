from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.order.models import Order
from app.modules.order.schemas import OrderCreate, OrderUpdate

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, order: OrderCreate) -> Order:
        db_order = Order(**order.model_dump())
        self.db.add(db_order)
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def get_by_id(self, order_id: int) -> Order | None:
        result = await self.db.execute(select(Order).filter(Order.id == order_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await self.db.execute(select(Order).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, order_id: int, order_update: OrderUpdate) -> Order | None:
        db_order = await self.get_by_id(order_id)
        if not db_order:
            return None
        
        update_data = order_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        
        await self.db.commit()
        await self.db.refresh(db_order)
        return db_order

    async def delete(self, order_id: int) -> bool:
        db_order = await self.get_by_id(order_id)
        if not db_order:
            return False
        
        await self.db.delete(db_order)
        await self.db.commit()
        return True
