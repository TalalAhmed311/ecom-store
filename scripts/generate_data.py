import csv
import random
import time
from uuid import uuid4
import os

def generate_products(filename="products.csv", count=1_000_000):
    print(f"Generating {count} products to {filename}...")
    start_time = time.time()
    
    # Check if directory exists
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["id", "name", "price", "inventory", "created_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Batch write for performance (though csv module is already buffered, this logic keeps memory low)
        for i in range(count):
            writer.writerow({
                "id": str(uuid4()),
                "name": f"Product {i + 1} - {''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))}",
                "price": round(random.uniform(10.0, 1000.0), 2),
                "inventory": random.randint(0, 10000),
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            if (i + 1) % 100000 == 0:
                print(f"Generated {i + 1} records...")

    end_time = time.time()
    print(f"Done! Generated {count} records in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    generate_products("scripts/products.csv")
