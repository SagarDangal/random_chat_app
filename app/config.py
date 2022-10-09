import os
from functools import lru_cache


class BaseConfig:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    DATABASE_CONNECT_DICT: dict = {}

    CORS_ALLOWED_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

    POST_API_HOST = os.environ.get('POST_API_HOST', 'http://128.199.83.162:8080/')     # Example http://<your_host>/api



class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class StagingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dist = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
        "staging": StagingConfig
    }

    config_name = os.environ.get("FAST_API_CONFIG", "dev")
    config_cls = config_cls_dist[config_name]
    return config_cls


settings = get_settings()
