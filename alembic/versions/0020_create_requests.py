"""020_create_requests

Revision ID: 0020_create_requests
Revises: 0019_create_transactions
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0020_create_requests"
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

    op.execute(
        """
        CREATE TABLE ad_requests (
            id         SERIAL NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            user_id    BIGINT NOT NULL,
            announ_id  INTEGER NOT NULL,
            format     TEXT NOT NULL,
            ad_text    TEXT NULL,
            ad_time    TIMESTAMP WITH TIME ZONE NOT NULL,
            CONSTRAINT ad_requests_pkey PRIMARY KEY (id),
            CONSTRAINT ad_requests_user_announ_key UNIQUE (user_id, announ_id),
            CONSTRAINT ad_requests_user_id_fkey FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT ad_requests_announ_id_fkey FOREIGN KEY (announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE ad_requests_media (
            id         SERIAL NOT NULL,
            request_id INTEGER NOT NULL,
            media_key  TEXT NOT NULL,
            CONSTRAINT ad_requests_media_pkey PRIMARY KEY (id),
            CONSTRAINT ad_requests_media_request_id_fkey FOREIGN KEY (request_id)
                REFERENCES ad_requests(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE ad_requests_buttons (
            id         SERIAL NOT NULL,
            request_id INTEGER NOT NULL,
            btn_text   TEXT NOT NULL,
            btn_url    TEXT NOT NULL,
            CONSTRAINT ad_requests_buttons_pkey PRIMARY KEY (id),
            CONSTRAINT ad_requests_buttons_request_id_fkey FOREIGN KEY (request_id)
                REFERENCES ad_requests(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_requests (
            id          SERIAL NOT NULL,
            created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
            user_id     BIGINT NOT NULL,
            announ_id   INTEGER NOT NULL,
            format      TEXT NOT NULL,
            story_text  TEXT NULL,
            story_media TEXT NOT NULL,
            story_time  TIMESTAMP WITH TIME ZONE NOT NULL,
            CONSTRAINT stories_requests_pkey PRIMARY KEY (id),
            CONSTRAINT stories_requests_user_announ_key UNIQUE (user_id, announ_id),
            CONSTRAINT stories_requests_user_id_fkey FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT stories_requests_announ_id_fkey FOREIGN KEY (announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE traffic_requests (
            id          SERIAL NOT NULL,
            created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
            user_id     BIGINT NOT NULL,
            announ_id   INTEGER NOT NULL,
            leads_count INTEGER NOT NULL,
            link        TEXT NOT NULL,
            price       NUMERIC(10,2) NOT NULL,
            CONSTRAINT traffic_requests_pkey PRIMARY KEY (id),
            CONSTRAINT traffic_requests_user_announ_key UNIQUE (user_id, announ_id),
            CONSTRAINT traffic_requests_user_id_fkey FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT traffic_requests_announ_id_fkey FOREIGN KEY (announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE traffic_requests;")
    op.execute("DROP TABLE stories_requests;")
    op.execute("DROP TABLE ad_requests_buttons;")
    op.execute("DROP TABLE ad_requests_media;")
    op.execute("DROP TABLE ad_requests;")
    op.execute("DROP TABLE chn_requests;")
