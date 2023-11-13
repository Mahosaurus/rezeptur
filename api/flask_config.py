"""Flask configuration."""
import os
from src.utils.helpers import get_repo_root

if os.environ.get("DEPLOY_ENV") == "production":
    ENV = 'development'
    FLASK_ENV = 'development'
    DEBUG = False
    Testing = False
else:
    ENV = 'development'
    FLASK_ENV = 'development'
    DEBUG = True
    Testing = True

POSTGRES_HOST       = os.environ.get("POSTGRES_HOST")
POSTGRES_DBNAME     = os.environ.get("POSTGRES_DBNAME")
POSTGRES_USER       = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD   = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_TABLE      = os.environ.get("POSTGRES_TABLE")
SECRET_KEY          = os.environ.get("SECRET")
