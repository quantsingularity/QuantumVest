"""Shared model helpers: UUID column type, default factories, JSON type."""

import os
import uuid

DATABASE_URL = os.environ.get("DATABASE_URL", "")
USE_POSTGRES = DATABASE_URL.startswith("postgresql") or DATABASE_URL.startswith(
    "postgres"
)

if USE_POSTGRES:  # pragma: no cover
    from sqlalchemy.dialects.postgresql import JSONB
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID

    JsonType = JSONB

    def uuid_col():
        return PG_UUID(as_uuid=True)

    def new_uuid():
        return uuid.uuid4()

else:
    from sqlalchemy import JSON, String  # noqa: F401

    JsonType = JSON

    def uuid_col():
        from app.extensions import db

        return db.String(36)

    def new_uuid():
        return str(uuid.uuid4())
