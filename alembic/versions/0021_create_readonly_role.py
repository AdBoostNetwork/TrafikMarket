"""021_create_readonly_role

Revision ID: 0021_create_readonly_role
Revises: 0020_create_requests
Create Date: 2026-07-24 00:00:00.000000

"""
import os
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0021_create_readonly_role"
down_revision: Union[str, Sequence[str], None] = "0020_create_requests"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    password = os.environ.get("AI_DB_PASSWORD", "")
    if not password:
        raise RuntimeError(
            "AI_DB_PASSWORD is not set — cannot create ai_readonly role without a password."
        )

    escaped_password = password.replace("'", "''")

    op.execute(
        f"""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='ai_readonly') THEN
                CREATE ROLE ai_readonly LOGIN PASSWORD '{escaped_password}';
            END IF;
        END $$;
        """
    )
    op.execute("GRANT CONNECT ON DATABASE traffmarket TO ai_readonly;")
    op.execute("GRANT USAGE ON SCHEMA public TO ai_readonly;")
    op.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO ai_readonly;")
    op.execute(
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ai_readonly;"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP OWNED BY ai_readonly;")
    op.execute("DROP ROLE IF EXISTS ai_readonly;")
