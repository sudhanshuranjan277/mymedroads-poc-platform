import os
from sqlalchemy import create_engine


DB_FOLDER = "database/sqlite"

os.makedirs(
    DB_FOLDER,
    exist_ok=True
)


DATABASE_URL = (
    "sqlite:///database/sqlite/mymedroads.db"
)


engine = create_engine(
    DATABASE_URL,
    echo=False
)