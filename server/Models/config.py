# Models/config.py

class Config:
    """Base config class with default settings."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    SQLALCHEMY_DATABASE_URI = "postgresql://pineapples:postgres@localhost/dev_ajali"
    DEBUG = True

class TestingConfig(Config):
    """Testing-specific configuration."""
    SQLALCHEMY_DATABASE_URI = "postgresql://pineapples:postgres@localhost/test_ajali"
    TESTING = True

class ProductionConfig(Config):
    """Production-specific configuration."""
    SQLALCHEMY_DATABASE_URI = "postgresql://pineapples:postgres@localhost/prod_ajali"
