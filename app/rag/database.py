
import os
import psycopg
from pathlib import Path
from dotenv import load_dotenv

# Explicitly locate .env in the project root
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


def get_connection():

    password = os.getenv("DB_PASSWORD")

    if not password:
        raise ValueError("DB_PASSWORD is missing from the .env file")

    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=password
    )

