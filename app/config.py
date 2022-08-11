import os

SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:3000/api/v1")
DEBUG = bool(os.environ.get("DEBUG", 0))
HOST = bool(os.environ.get("HOST", "0.0.0.0"))
PORT = bool(os.environ.get("PORT", "5000"))
