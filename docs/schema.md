# Database Schema Design

## Tables

### 1. Products
Stores product information.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary Key |
| name | VARCHAR(255) | Product Name |
| price | DECIMAL(10, 2) | Product Price |
| created_at | TIMESTAMP | Creation Timestamp |

### 2. Inventory
Stores inventory count for products. Separate table to handle high concurrency updates.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary Key |
| product_id | UUID | Foreign Key to Products.id |
| quantity | INTEGER | Available quantity |
| last_updated | TIMESTAMP | Last update timestamp |

### 3. Orders
Stores order information.

| Column | Type | Description |
|---|---|---|
| id | UUID | Primary Key |
| product_id | UUID | Foreign Key to Products.id |
| quantity | INTEGER | Ordered quantity |
| total_price | DECIMAL(10, 2) | Total price of the order |
| status | VARCHAR(50) | Order status (PENDING, COMPLETED, CANCELLED) |
| created_at | TIMESTAMP | Creation Timestamp |

## Relationships
- One Product can have one Inventory record (1:1).
- One Product can be in many Orders (1:N).
