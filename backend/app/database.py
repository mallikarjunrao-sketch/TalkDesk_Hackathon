from typing import Generator
from sqlmodel import Session, SQLModel, create_engine, text
from backend.app.config import settings

# SQLite requires check_same_thread: False when accessed by multiple threads in FastAPI
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,
    connect_args=connect_args,
)


def init_db() -> None:
    """Create all database tables defined in SQLModel metadata."""
    # Importing models registers them with SQLModel.metadata
    import backend.app.models  # noqa: F401
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency that yields a database session."""
    with Session(engine) as session:
        yield session


def check_database_connection() -> bool:
    """Perform a live check to verify database connectivity.

    Executes a lightweight query against the active database engine.
    Returns True if connection succeeds and query evaluates, False otherwise.
    """
    try:
        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
            return result is not None
    except Exception:
        return False

