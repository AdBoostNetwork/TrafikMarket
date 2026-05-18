"""001_create_users_table

Revision ID: 2e48773d7daf
Revises: 
Create Date: 2026-05-14 13:23:17.949085

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '2e48773d7daf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE users (
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            current_balance NUMERIC(10,2) NOT NULL DEFAULT 0,
            success_count INTEGER NOT NULL DEFAULT 0,
            ref_link TEXT NOT NULL,
            referrer_id BIGINT NULL,
            is_banned BOOLEAN NOT NULL DEFAULT FALSE,
            avatar_filename TEXT NULL,
            good_marks INTEGER NOT NULL DEFAULT 0,
            bad_marks INTEGER NOT NULL DEFAULT 0,
            reg_date DATE NOT NULL,
            vip_status INTEGER NOT NULL DEFAULT 0,
            theme_mode BOOLEAN NOT NULL,
            deals_summ NUMERIC(10,2) NOT NULL DEFAULT 0,
            frozen_balance NUMERIC(10,2) NOT NULL DEFAULT 0,
            was_online TIMESTAMP WITH TIME ZONE NOT NULL,
            wallpaper_id INTEGER NULL,
            CONSTRAINT users_pkey PRIMARY KEY (user_id),
            CONSTRAINT users_referrer_id_fkey FOREIGN KEY (referrer_id)
                REFERENCES users(user_id)
                ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE users;")
