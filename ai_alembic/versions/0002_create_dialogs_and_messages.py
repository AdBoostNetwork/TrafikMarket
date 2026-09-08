"""0002_create_dialogs_and_messages

Revision ID: 0002_create_dialogs_and_messages
Revises: 0001_baseline
Create Date: 2026-07-29 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0002_create_dialogs_and_messages"
down_revision: Union[str, Sequence[str], None] = "0001_baseline"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE dialogs (
            id              BIGSERIAL NOT NULL,
            user_id         BIGINT NOT NULL,
            last_message_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            CONSTRAINT dialogs_pkey PRIMARY KEY (id)
        );
        """
    )

    op.execute(
        "CREATE INDEX dialogs_user_last_msg_idx ON dialogs (user_id, last_message_at DESC);"
    )

    op.execute(
        """
        CREATE TABLE messages (
            id        BIGSERIAL NOT NULL,
            dialog_id BIGINT NOT NULL,
            role      VARCHAR(16) NOT NULL,
            content   TEXT NOT NULL,
            CONSTRAINT messages_pkey PRIMARY KEY (id),
            CONSTRAINT messages_role_check CHECK (role IN ('user', 'assistant')),
            CONSTRAINT messages_dialog_id_fkey FOREIGN KEY (dialog_id)
                REFERENCES dialogs(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        "CREATE INDEX messages_dialog_id_idx ON messages (dialog_id, id);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE messages;")
    op.execute("DROP TABLE dialogs;")
