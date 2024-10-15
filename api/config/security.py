__all__ = ["token_expiration_time", "allowed_origins"]

from datetime import timedelta

from .__base_config import BACKEND_DOMAIN, FRONTEND_DOMAIN

token_expiration_time = timedelta(days=1)

allowed_origins = [
    f"http://{BACKEND_DOMAIN}",
    f"http://{FRONTEND_DOMAIN}",
    f"https://{BACKEND_DOMAIN}",
    f"https://{FRONTEND_DOMAIN}",
]
