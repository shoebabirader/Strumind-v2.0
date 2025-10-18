from sqlalchemy import create_engine, event, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os
import logging

logger = logging.getLogger(__name__)

# SECURITY FIX: Configure engine with connection pooling and resource management
if settings.DATABASE_URL.startswith('sqlite'):
    # SQLite configuration
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},  # Needed for SQLite
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600,   # Recycle connections after 1 hour
        echo=False,          # Disable SQL logging in production
    )
else:
    # PostgreSQL configuration with connection pooling
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,              # Maximum number of connections
        max_overflow=20,           # Maximum overflow connections
        pool_timeout=30,           # Timeout for getting connection
        pool_recycle=3600,         # Recycle connections after 1 hour
        pool_pre_ping=True,        # Verify connections before using
        echo=False,                # Disable SQL logging in production
        poolclass=pool.QueuePool,  # Use queue-based pool
    )

# SECURITY FIX: Add connection event listeners for monitoring
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Log new database connections"""
    logger.debug("New database connection established")

@event.listens_for(engine, "close")
def receive_close(dbapi_conn, connection_record):
    """Log closed database connections"""
    logger.debug("Database connection closed")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
        print("   Core features will still work without database")
        return False
