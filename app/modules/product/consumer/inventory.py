import asyncio
import json
from aiokafka import AIOKafkaConsumer
from app.common.config import settings
from app.common.database import AsyncSessionLocal
from app.modules.product.models import Inventory
from sqlalchemy import select, update

async def consume_orders():
    consumer = AIOKafkaConsumer(
        "order_created",
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id="inventory_group",
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            order_data = msg.value
            print(f"Received order: {order_data}")
            product_id = order_data.get("product_id")
            quantity = order_data.get("quantity")
            
            if not product_id or not quantity:
                continue
                
            async with AsyncSessionLocal() as session:
                # Update inventory
                # We need to handle concurrency ideally, but simple update is fine for now
                stmt = (
                    update(Inventory)
                    .where(Inventory.product_id == product_id)
                    .values(quantity=Inventory.quantity - quantity)
                )
                await session.execute(stmt)
                await session.commit()
                print(f"Updated inventory for product {product_id} by -{quantity}")
                
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_orders())
