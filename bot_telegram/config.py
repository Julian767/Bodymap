"""Configuración compartida entre la web y el bot de Telegram."""
import os
from pathlib import Path


BOT_USERNAME = "Bodymap_julian_bot"

_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def _load_env():
    """Carga KEY=VALUE desde .env sin sobrescribir variables del sistema."""
    if not _ENV_PATH.is_file():
        return

    for line in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


_load_env()

# El token se lee del entorno (o del .env). Nunca queda en el código fuente.
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
