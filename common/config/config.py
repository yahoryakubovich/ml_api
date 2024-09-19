from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str = None
    port: int = None
    user: str = None
    password: str = None
    name: str = None

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="POSTGRES_", extra="ignore")


class RedisSettings(BaseSettings):
    host: str = None
    port: int = None
    name: str = None

    @property
    def redis_url(self):
        return f"{self.host}://{self.name}:{self.port}"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="REDIS_", extra="ignore")


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
