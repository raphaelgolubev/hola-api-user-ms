import uvicorn

from src.config import settings
import src.logging # noqa


print("SETTINGS: ", settings.app.model_dump(), "\n", settings.db.model_dump())


uvicorn.run(
    'src.application:app',
    host=settings.app.host,
    port=settings.app.port,
    timeout_keep_alive=30,
    lifespan='on',
    reload=True,
)