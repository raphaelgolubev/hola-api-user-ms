from fastapi import FastAPI

from src.database.tables import create_all, drop_all
from src.routing import main_router

from src.logging import logger


async def startup():
    logger.info("Starting up...")
    try:
        await create_all()
    except Exception as e:
        logger.error(f"Error during tables creating: {str(e)}")
    else:
        logger.success(f"Connected to database, tables created")


async def shutdown():
    logger.info("Shutting down...")
    try:
        await drop_all()
    except Exception as e:
        logger.error(f"Error during dropping tables: {str(e)}")
    else:
        logger.success("Disconnected from database")


async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router, prefix="/api/v1")