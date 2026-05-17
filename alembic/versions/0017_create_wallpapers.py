"""017_create_wallpapers

Revision ID: 0017_create_wallpapers
Revises: 0016_create_rate
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0017_create_wallpapers"
down_revision: Union[str, Sequence[str], None] = "0016_create_rate"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE wallpapers (
            id             SERIAL NOT NULL,
            wallpaper_name TEXT NOT NULL,
            img_key        TEXT NOT NULL,
            CONSTRAINT wallpapers_pkey PRIMARY KEY (id),
            CONSTRAINT wallpapers_wallpaper_name_key UNIQUE (wallpaper_name),
            CONSTRAINT wallpapers_img_key_key UNIQUE (img_key)
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE wallpapers;")
