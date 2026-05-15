"""014_create_stories_nets

Revision ID: 0014_create_stories_nets
Revises: 0013_create_stories
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0014_create_stories_nets"
down_revision: Union[str, Sequence[str], None] = "0013_create_stories"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE stories_nets (
            story_id     INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            CONSTRAINT stories_nets_pkey PRIMARY KEY (story_id),
            CONSTRAINT stories_nets_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_nets_links (
            id          SERIAL NOT NULL,
            story_id    INTEGER NOT NULL,
            link        TEXT NOT NULL,
            red_label   BOOLEAN NOT NULL DEFAULT FALSE,
            black_label BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT stories_nets_links_pkey PRIMARY KEY (id),
            CONSTRAINT stories_nets_links_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES stories_nets(story_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_nets_prices (
            id       SERIAL NOT NULL,
            story_id INTEGER NOT NULL,
            format   TEXT NOT NULL,
            price    NUMERIC(10,2) NOT NULL,
            CONSTRAINT stories_nets_prices_pkey PRIMARY KEY (id),
            CONSTRAINT stories_nets_prices_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES stories_nets(story_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_nets_topics (
            story_id INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            CONSTRAINT stories_nets_topics_pkey PRIMARY KEY (story_id, topic_id),
            CONSTRAINT stories_nets_topics_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES stories_nets(story_id) ON DELETE CASCADE,
            CONSTRAINT stories_nets_topics_topic_id_fkey FOREIGN KEY (topic_id)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE stories_nets_countries (
            story_id   INTEGER NOT NULL,
            country_id INTEGER NOT NULL,
            CONSTRAINT stories_nets_countries_pkey PRIMARY KEY (story_id, country_id),
            CONSTRAINT stories_nets_countries_story_id_fkey FOREIGN KEY (story_id)
                REFERENCES stories_nets(story_id) ON DELETE CASCADE,
            CONSTRAINT stories_nets_countries_country_id_fkey FOREIGN KEY (country_id)
                REFERENCES countries(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE stories_nets_countries;")
    op.execute("DROP TABLE stories_nets_topics;")
    op.execute("DROP TABLE stories_nets_prices;")
    op.execute("DROP TABLE stories_nets_links;")
    op.execute("DROP TABLE stories_nets;")
