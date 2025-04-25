"""A module providing database access."""

import asyncio
from datetime import datetime

import databases
import sqlalchemy
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import (    # type: ignore
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from sqlalchemy.dialects.postgresql import UUID

from cinemaapi.config import config

metadata = sqlalchemy.MetaData()

movie_table = sqlalchemy.Table(
    "movies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, unique=True),
    sqlalchemy.Column("genre", sqlalchemy.String),
    sqlalchemy.Column("age_restriction", sqlalchemy.Integer),
    sqlalchemy.Column("duration", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("rating", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)


review_table = sqlalchemy.Table(
    "reviews",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
    sqlalchemy.Column("comment", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column(
        "movie_id",
        sqlalchemy.ForeignKey("movies.id"),
        nullable=False),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

repertoire_table = sqlalchemy.Table(
    "repertoires",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

showing_table = sqlalchemy.Table(
    "showings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("language_ver", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("date", sqlalchemy.types.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column(
        "repertoire_id",
        sqlalchemy.ForeignKey("repertoires.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "movie_id",
        sqlalchemy.ForeignKey("movies.id"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "hall_id",
        sqlalchemy.ForeignKey("halls.id"),
        nullable=True,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

hall_table = sqlalchemy.Table(
    "halls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("alias", sqlalchemy.String, unique=True),
    sqlalchemy.Column("seat_amount", sqlalchemy.Integer),
    sqlalchemy.Column("row_amount", sqlalchemy.Integer),
    sqlalchemy.Column("seats", sqlalchemy.JSON),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

reservation_table = sqlalchemy.Table(
    "reservations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("seat_row", sqlalchemy.String),
    sqlalchemy.Column("seat_num", sqlalchemy.String),
    sqlalchemy.Column(
        "showing_id",
        sqlalchemy.ForeignKey("showings.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("privilege", sqlalchemy.String),
)

db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")