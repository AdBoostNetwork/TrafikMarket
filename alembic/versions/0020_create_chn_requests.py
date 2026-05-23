"""020_create_chn_requests

Revision ID: 0020_create_chn_requests
Revises: 0019_create_transactions
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0020_create_chn_requests"
down_revision: Union[str, Sequence[str], None] = "0019_create_transactions"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE chn_requests (
            id          SERIAL NOT NULL,
            created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
            user_id     BIGINT NOT NULL,
            announ_id   INTEGER NOT NULL,
            tg_username TEXT NOT NULL,
            CONSTRAINT chn_requests_pkey PRIMARY KEY (id),
            CONSTRAINT chn_requests_user_announ_key UNIQUE (user_id, announ_id),
            CONSTRAINT chn_requests_user_id_fkey FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT chn_requests_announ_id_fkey FOREIGN KEY (announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE chn_requests;")
