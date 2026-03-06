from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.order.repository import OrderRepository
from app.modules.order.schemas import OrderCreate, OrderUpdate
from app.modules.order.models import Order

class OrderService:
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def create_order(self, order_data: OrderCreate) -> Order:
        order = await self.repository.create(order_data)
        # Publish event
        from app.modules.order.producer.service import publish_order_created
        await publish_order_created({
            "id": order.id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "status": order.status
        })
        return order

    async def get_order(self, order_id: int) -> Order | None:
        return await self.repository.get_by_id(order_id)

    async def list_orders(self, skip: int = 0, limit: int = 100) -> list[Order]:
        return await self.repository.get_all(skip, limit)

    async def update_order(self, order_id: int, order_data: OrderUpdate) -> Order | None:
        return await self.repository.update(order_id, order_data)

    async def delete_order(self, order_id: int) -> bool:
        return await self.repository.delete(order_id)
