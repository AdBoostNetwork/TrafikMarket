"""013_create_stories

Revision ID: 0013_create_stories
Revises: 0012_create_max_net_ads
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0013_create_stories"
down_revision: Union[str, Sequence[str], None] = "0012_create_max_net_ads"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE stories (
            story_id     INTEGER NOT NULL,
            link         TEXT NOT NULL,
            topic        INTEGER NOT NULL,
            country      INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            red_label    BOOLEAN NOT NULL DEFAULT FALSE,
            black_label  BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT stories_pkey PRIMARY KEY (story_id),
            CONSTRAINT stories_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE,
            CONSTRAINT stories_topic_fkey FOREIGN KEY (topic)
                REFERENCES topics(id) ON DELETE CASCADE,
            CONSTRAINT stories_country_fkey FOREIGN KEY (country)
                REFERENCES countries(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_prices (
            id       SERIAL NOT NULL,
            story_id INTEGER NOT NULL,
            format   TEXT NOT NULL,
            price    NUMERIC(10,2) NOT NULL,
            CONSTRAINT stories_prices_pkey PRIMARY KEY (id),
            CONSTRAINT stories_prices_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES stories(story_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE stories_prices;")
    op.execute("DROP TABLE stories;")
