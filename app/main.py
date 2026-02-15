from fastapi import FastAPI
from app.modules.order.controller import router as order_router
from app.common.config import settings

app = FastAPI(title="E-commerce Store API")

app.include_router(order_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to E-commerce Store API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
