from dotenv import find_dotenv, load_dotenv

from pinkiepie_trading.app import create_app
from pinkiepie_trading.config import Config

try:
    load_dotenv(find_dotenv(".env"), override=False)
except IOError:
    pass


__all__ = ("app",)

# Load config from env.
config = Config()

# Create trading app.
app = create_app(config=config)

# Config Celery.
