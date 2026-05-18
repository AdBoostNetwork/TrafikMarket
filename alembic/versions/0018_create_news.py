"""018_create_news

Revision ID: 0018_create_news
Revises: 0017_create_wallpapers
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0018_create_news"
down_revision: Union[str, Sequence[str], None] = "0017_create_wallpapers"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE news (
            id        SERIAL NOT NULL,
            news_name TEXT NOT NULL,
            news_text TEXT NOT NULL,
            CONSTRAINT news_pkey PRIMARY KEY (id)
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE news;")
