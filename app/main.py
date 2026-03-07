from fastapi import FastAPI
from app.modules.order.controller import router as order_router
from app.modules.product.controller import router as product_router
from app.common.config import settings

from contextlib import asynccontextmanager
from app.common.kafka import kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        import asyncio
        # Try to connect with timeout
        await asyncio.wait_for(kafka_producer.start(), timeout=2.0)
        print("Kafka producer started")
    except Exception as e:
        print(f"Failed to start Kafka producer: {e}")
    yield
    # Shutdown
    try:
        await kafka_producer.stop()
    except Exception:
        pass

app = FastAPI(title="E-commerce Store API", lifespan=lifespan)

app.include_router(product_router)
app.include_router(order_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce Store API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

