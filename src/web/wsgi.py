import os
from src.web.api import create_app

app = create_app(os.getenv("APP_SETTINGS") or "config.DevConfig")

if __name__ == "__main__":
    app.run()
