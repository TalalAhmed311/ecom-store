from app.modules.product.repository import ProductRepository
from app.modules.product.schemas import ProductResponse

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def get_products(self, skip: int = 0, limit: int = 10):
        products = await self.repository.get_all(skip, limit)
        # Transform to Pydantic models
        # Note: inventory is a relationship, so product.inventory is an Inventory object
        return [
            ProductResponse(
                id=product.id,
                name=product.name,
                price=product.price,
                created_at=product.created_at,
                inventory_quantity=product.inventory.quantity if product.inventory else 0
            ) 
            for product in products
        ]

    async def get_product(self, product_id: str):
        product = await self.repository.get_by_id(product_id)
        if not product:
            return None
        return ProductResponse(
            id=product.id,
            name=product.name,
            price=product.price,
            created_at=product.created_at,
            inventory_quantity=product.inventory.quantity if product.inventory else 0
        )
