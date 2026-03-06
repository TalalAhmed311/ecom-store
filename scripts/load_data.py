import asyncio
import csv
import os
import time
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.common.config import settings

async def load_data(filename="scripts/products.csv"):
    print(f"Loading data from {filename}...")
    start_time = time.time()
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return

    # Use raw connection for COPY
    engine = create_async_engine(settings.DATABASE_URL)
    
    async with engine.connect() as conn:
        # We need raw DBAPI connection for COPY
        # asyncpg connection is accessible via:
        raw_conn = await conn.get_raw_connection()
        # raw_conn is an AdaptedConnection (SqlAlchemy wrapper), .driver_connection is the asyncpg connection
        pg_conn = raw_conn.driver_connection
        
        # Determine absolute path for COPY (must be accessible by server if using COPY FROM 'file')
        # But we are in a container environment possibly? No, script is running on host, DB in container.
        # DB container cannot see host file unless mounted.
        # So we should use COPY FROM STDIN.
        
        with open(filename, 'r') as f:
            # Skip header if present (my generate_data.py adds header)
            # asyncpg copy_to_table(table_name, source, columns=None, ...)
            # source can be a file-like object or an iterable.
            
            # Read first line to check header
            # Actually asyncpg copy_records_to_table is easier for list of tuples, 
            # but copy_from is for file-like.
            
            # Skip incorrect direct copy
            # await pg_conn.copy_to_table(...)
            
            # Now populate inventory table.
            # Since inventory is 1:1 and we generated "inventory" column in CSV,
            # we need to split this.
            # My CSV has: id, name, price, inventory, created_at
            # Product table: id, name, price, created_at
            # Inventory table: product_id (fk), quantity
            
            # The COPY command above will fail because 'inventory' column does not exist in 'products' table.
            # I should have generated two CSVs or load into a temp table then split.
            
            # Strategy:
            # 1. Create a temp table matching CSV structure.
            # 2. COPY CSV to temp table.
            # 3. Insert into products from temp table.
            # 4. Insert into inventory from temp table.
            # 5. Drop temp table.
            
            print("Creating temp table...")
            await conn.execute(text("""
                CREATE TEMP TABLE temp_products (
                    id VARCHAR PRIMARY KEY,
                    name VARCHAR,
                    price FLOAT,
                    inventory INTEGER,
                    created_at TIMESTAMP
                )
            """))
            
            print("Copying to temp table...")
            f.seek(0) # Reset file pointer
            await pg_conn.copy_to_table(
                'temp_products',
                source=f,
                columns=['id', 'name', 'price', 'inventory', 'created_at'],
                format='csv',
                header=True
            )
            
            print("Inserting into products...")
            await conn.execute(text("""
                INSERT INTO products (id, name, price, created_at)
                SELECT id, name, price, created_at FROM temp_products
                ON CONFLICT (id) DO NOTHING
            """))
            
            print("Inserting into inventory...")
            await conn.execute(text("""
                INSERT INTO inventory (product_id, quantity)
                SELECT id, inventory FROM temp_products
                ON CONFLICT (product_id) DO NOTHING
            """))
            
            print("Cleaning up...")
            await conn.execute(text("DROP TABLE temp_products"))
            await conn.commit()

    await engine.dispose()
    end_time = time.time()
    print(f"Done! Loaded data in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(load_data())
