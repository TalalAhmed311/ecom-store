# E-commerce Store API

A modular, high-performance E-commerce API built with FastAPI, PostgreSQL, MongoDB, Redis, and Kafka.

## Features

- **Modular Architecture**: Services are isolated in `app/modules` (e.g., `order`), facilitating future microservices migration.
- **Async First**: Built on FastAPI with `asyncpg` and `motor` for high concurrency.
- **Hybrid Database**: Uses PostgreSQL for relational data (Orders) and MongoDB for unstructured data.
- **Event Driven**: Integrated with Kafka for asynchronous service communication.
- **Containerized**: Full development environment with Docker Compose.

## Tech Stack

- **Framework**: FastAPI
- **Databases**: PostgreSQL, MongoDB, Redis
- **Messaging**: Kafka (KRaft mode)
- **Deployment**: Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose installed.

### Setup & Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ecom-store
    ```

2.  **Start Services:**
    ```bash
    docker-compose up -d --build
    ```
    This will start the FastAPI app, Postgres, Redis, Mongo, and Kafka.

3.  **Access the API:**
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

4.  **Database Migrations:**
    To apply database migrations:
    ```bash
    docker-compose exec app alembic revision --autogenerate -m "Initial migration"
    docker-compose exec app alembic upgrade head
    ```

## Development

- **Directory Structure**:
    - `app/common`: Shared utilities and database connections.
    - `app/modules`: Feature modules (e.g., `order`). Each module describes its own Controller, Service, and Repository.
    - `alembic`: Database migrations.

- **Adding a New Module**:
    1. Create a folder in `app/modules/`.
    2. Define `models.py`, `schemas.py`, `repository.py`, `service.py`, and `controller.py`.
    3. Register the router in `app/main.py`.

## Configuration

Environment variables are managed via `pydantic-settings` in `app/common/config.py`.
Defaults are set for the Docker environment.

| Variable | Default (Docker) | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql+asyncpg://user:password@postgres:5432/ecom_db` | Postgres Connection |
| `REDIS_URL` | `redis://redis:6379/0` | Redis Connection |
| `MONGO_URL` | `mongodb://mongo:27017/ecom_mongo` | Mongo Connection |
| `KAFKA_BOOTSTRAP_SERVERS` | `kafka:9092` | Kafka Brokers |

## License

MIT
