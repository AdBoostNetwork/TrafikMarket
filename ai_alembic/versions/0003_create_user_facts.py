"""0003_create_user_facts

Revision ID: 0003_create_user_facts
Revises: 0002_create_dialogs_and_messages
Create Date: 2026-07-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0003_create_user_facts"
down_revision: Union[str, Sequence[str], None] = "0002_create_dialogs_and_messages"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE user_facts (
            id      BIGSERIAL NOT NULL,
            user_id BIGINT NOT NULL,
            content TEXT NOT NULL,
            CONSTRAINT user_facts_pkey PRIMARY KEY (id)
        );
        """
    )

    op.execute(
        "CREATE INDEX user_facts_user_id_idx ON user_facts (user_id);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE user_facts;")
