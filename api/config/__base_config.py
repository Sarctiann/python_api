__all__ = [
    "MONGODB_URI",
    "logger",
    "SECRET_KEY",
    "BACKEND_DOMAIN",
    "FRONTEND_DOMAIN",
]

import logging
import os

from dotenv import load_dotenv

# Cargamos nuestras variables de entorno
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_CONNECTION_STRING")
if not MONGODB_URI:
    raise Exception("MongoDB connection string not found")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("Secret key not found")

BACKEND_DOMAIN = os.getenv("BACKEND_DOMAIN")
if not BACKEND_DOMAIN:
    raise Exception("Backend domain not found")

FRONTEND_DOMAIN = os.getenv("FRONTEND_DOMAIN")
if not FRONTEND_DOMAIN:
    raise Exception("Frontend domain not found")


logger = logging.getLogger("uvicorn")
# logger.setLevel(logging.DEBUG)

# Fixing a "bycript issue"
logging.getLogger("passlib").setLevel(logging.ERROR)
