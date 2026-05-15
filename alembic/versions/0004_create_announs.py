"""004_create_announs

Revision ID: 0004_create_announs
Revises: 0003_seed_dictionaries
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0004_create_announs"
down_revision: Union[str, Sequence[str], None] = "0003_seed_dictionaries"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE announ_types (
            id   SERIAL NOT NULL,
            type_name TEXT NOT NULL,
            CONSTRAINT announ_types_pkey PRIMARY KEY (id),
            CONSTRAINT announ_types_type_name_key UNIQUE (type_name)
        );
        """
    )

    op.execute("CREATE SEQUENCE announs_article_seq START WITH 30000;")

    op.execute(
        """
        CREATE TABLE announs (
            announ_id  SERIAL NOT NULL,
            seller_id  BIGINT NOT NULL,
            type       INTEGER NOT NULL,
            title      VARCHAR(50) NOT NULL,
            short_text VARCHAR(128) NOT NULL,
            long_text  VARCHAR(1024) NULL,
            status     VARCHAR(16) NOT NULL,
            article    BIGINT NOT NULL DEFAULT nextval('announs_article_seq'),
            CONSTRAINT announs_pkey PRIMARY KEY (announ_id),
            CONSTRAINT announs_article_key UNIQUE (article),
            CONSTRAINT announs_seller_id_fkey FOREIGN KEY (seller_id)
                REFERENCES users(user_id) ON DELETE CASCADE,
            CONSTRAINT announs_type_fkey FOREIGN KEY (type)
                REFERENCES announ_types(id) ON DELETE CASCADE
        );
        """
    )

    op.execute("ALTER SEQUENCE announs_article_seq OWNED BY announs.article;")

    op.execute(
        """
        CREATE TABLE images (
            id            BIGSERIAL NOT NULL,
            img_announ_id INTEGER NOT NULL,
            img_key       TEXT NOT NULL,
            CONSTRAINT images_pkey PRIMARY KEY (id),
            CONSTRAINT images_img_announ_id_fkey FOREIGN KEY (img_announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE images;")
    op.execute("DROP TABLE announs;")
    op.execute("DROP SEQUENCE IF EXISTS announs_article_seq;")
    op.execute("DROP TABLE announ_types;")
