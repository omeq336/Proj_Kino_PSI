"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from cinemaapi.api.routers.movie import router as movie_router
from cinemaapi.api.routers.review import router as review_router
from cinemaapi.api.routers.repertoire import router as repertoire_router
from cinemaapi.api.routers.showing import router as showing_router
from cinemaapi.api.routers.hall import router as hall_router
from cinemaapi.api.routers.reservation import router as reservation_router
from cinemaapi.container import Container
from cinemaapi.db import database
from cinemaapi.db import init_db
from cinemaapi.api.routers.user import router as user_router

container = Container()
container.wire(modules=[
    "cinemaapi.api.routers.movie",
    "cinemaapi.api.routers.review",
    "cinemaapi.api.routers.repertoire",
    "cinemaapi.api.routers.showing",
    "cinemaapi.api.routers.hall",
    "cinemaapi.api.routers.reservation",
    "cinemaapi.api.routers.user",
])


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(movie_router, prefix="/movie")
app.include_router(review_router, prefix="/review")
app.include_router(repertoire_router, prefix="/repertoire")
app.include_router(showing_router, prefix="/showing")
app.include_router(hall_router, prefix="/hall")
app.include_router(reservation_router, prefix="/reservation")
app.include_router(user_router, prefix="")

@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)