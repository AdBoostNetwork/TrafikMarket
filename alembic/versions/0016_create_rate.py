"""016_create_rate

Revision ID: 0016_create_rate
Revises: 0015_create_traffic
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0016_create_rate"
down_revision: Union[str, Sequence[str], None] = "0015_create_traffic"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE rate (
            id               SERIAL NOT NULL,
            ruble_usdt_rate  NUMERIC(10,2) NOT NULL,
            CONSTRAINT rate_pkey PRIMARY KEY (id),
            CONSTRAINT rate_single_row CHECK (id = 1)
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE rate;")
