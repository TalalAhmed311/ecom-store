from app.common.kafka import kafka_producer

async def publish_order_created(order_dict: dict):
    # Ensure producer is started (handled in main startup usually, or lazily)
    # Ideally should be started on app startup.
    await kafka_producer.send("order_created", order_dict)
