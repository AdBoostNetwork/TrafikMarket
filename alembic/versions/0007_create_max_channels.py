"""007_create_max_channels

Revision ID: 0007_create_max_channels
Revises: 0006_create_chns_nets
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0007_create_max_channels"
down_revision: Union[str, Sequence[str], None] = "0006_create_chns_nets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE max_channels (
            chn_announ_id  INTEGER NOT NULL,
            link           TEXT NOT NULL,
            price          NUMERIC(10,2) NOT NULL,
            chn_type       BOOLEAN NULL,
            topic          INTEGER NOT NULL,
            subs_count     INTEGER NULL,
            cover_count    NUMERIC(10,2) NULL,
            err            NUMERIC(10,2) NULL,
            profitability  NUMERIC(10,2) NULL,
            on_requests    BOOLEAN NOT NULL,
            requests_count INTEGER NULL,
            author         BOOLEAN NOT NULL,
            CONSTRAINT max_channels_pkey PRIMARY KEY (chn_announ_id),
            CONSTRAINT max_channels_chn_announ_id_fkey FOREIGN KEY (chn_announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE,
            CONSTRAINT max_channels_topic_fkey FOREIGN KEY (topic)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE max_channels;")
