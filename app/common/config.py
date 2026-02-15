from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/ecom_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    MONGO_URL: str = "mongodb://localhost:27017/ecom_mongo"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    class Config:
        env_file = ".env"

settings = Settings()
