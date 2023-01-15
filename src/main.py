import logging.config
from subprocess import Popen
import sys, os
from pathlib import Path
from fastapi import FastAPI

ROOT = Path(__file__).parent.parent.resolve()
if not str(ROOT) in sys.path:
    sys.path.insert(0, str(ROOT))
from src.interface.authorization_routers import auth_router


# logging
logging.config.fileConfig(
    str(ROOT.joinpath("logging.conf")), disable_existing_loggers=False
)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(auth_router)


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8765)

    if (SSL_KEYFILE := os.getenv("SSL_KEYFILE")) and (
        SSL_CERTFILE := os.getenv("SSL_CERTFILE")
    ):

        Popen(["python", "-m", "https_redirect"])

        uvicorn.run(
            "main:app",
            host=str(HOST),
            port=443,
            log_level="info",
            ssl_keyfile=SSL_KEYFILE,
            ssl_certfile=SSL_CERTFILE,
        )
    else:
        uvicorn.run(
            "main:app",
            host=str(HOST),
            port=int(PORT),
            log_level="info",
        )
