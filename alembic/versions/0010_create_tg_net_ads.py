"""010_create_tg_net_ads

Revision ID: 0010_create_tg_net_ads
Revises: 0009_create_tg_ads
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0010_create_tg_net_ads"
down_revision: Union[str, Sequence[str], None] = "0009_create_tg_ads"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE tg_net_ads (
            ad_id        INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            CONSTRAINT tg_net_ads_pkey PRIMARY KEY (ad_id),
            CONSTRAINT tg_net_ads_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_net_ads_links (
            id          SERIAL NOT NULL,
            ad_id       INTEGER NOT NULL,
            link        TEXT NOT NULL,
            red_label   BOOLEAN NOT NULL DEFAULT FALSE,
            black_label BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT tg_net_ads_links_pkey PRIMARY KEY (id),
            CONSTRAINT tg_net_ads_links_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_net_ads_prices (
            id     SERIAL NOT NULL,
            ad_id  INTEGER NOT NULL,
            format TEXT NOT NULL,
            price  NUMERIC(10,2) NOT NULL,
            CONSTRAINT tg_net_ads_prices_pkey PRIMARY KEY (id),
            CONSTRAINT tg_net_ads_prices_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_net_ads_topics (
            ad_id    INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            CONSTRAINT tg_net_ads_topics_pkey PRIMARY KEY (ad_id, topic_id),
            CONSTRAINT tg_net_ads_topics_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE,
            CONSTRAINT tg_net_ads_topics_topic_id_fkey FOREIGN KEY (topic_id)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_net_ads_countries (
            ad_id      INTEGER NOT NULL,
            country_id INTEGER NOT NULL,
            CONSTRAINT tg_net_ads_countries_pkey PRIMARY KEY (ad_id, country_id),
            CONSTRAINT tg_net_ads_countries_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES tg_net_ads(ad_id) ON DELETE CASCADE,
            CONSTRAINT tg_net_ads_countries_country_id_fkey FOREIGN KEY (country_id)
                REFERENCES countries(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE tg_net_ads_countries;")
    op.execute("DROP TABLE tg_net_ads_topics;")
    op.execute("DROP TABLE tg_net_ads_prices;")
    op.execute("DROP TABLE tg_net_ads_links;")
    op.execute("DROP TABLE tg_net_ads;")
