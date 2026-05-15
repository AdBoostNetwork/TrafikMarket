"""012_create_max_net_ads

Revision ID: 0012_create_max_net_ads
Revises: 0011_create_max_ads
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0012_create_max_net_ads"
down_revision: Union[str, Sequence[str], None] = "0011_create_max_ads"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE max_net_ads (
            ad_id        INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            CONSTRAINT max_net_ads_pkey PRIMARY KEY (ad_id),
            CONSTRAINT max_net_ads_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_net_ads_links (
            id    SERIAL NOT NULL,
            ad_id INTEGER NOT NULL,
            link  TEXT NOT NULL,
            CONSTRAINT max_net_ads_links_pkey PRIMARY KEY (id),
            CONSTRAINT max_net_ads_links_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES max_net_ads(ad_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_net_ads_prices (
            id     SERIAL NOT NULL,
            ad_id  INTEGER NOT NULL,
            format TEXT NOT NULL,
            price  NUMERIC(10,2) NOT NULL,
            CONSTRAINT max_net_ads_prices_pkey PRIMARY KEY (id),
            CONSTRAINT max_net_ads_prices_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES max_net_ads(ad_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_net_ads_topics (
            ad_id    INTEGER NOT NULL,
            topic_id INTEGER NOT NULL,
            CONSTRAINT max_net_ads_topics_pkey PRIMARY KEY (ad_id, topic_id),
            CONSTRAINT max_net_ads_topics_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES max_net_ads(ad_id) ON DELETE CASCADE,
            CONSTRAINT max_net_ads_topics_topic_id_fkey FOREIGN KEY (topic_id)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE max_net_ads_topics;")
    op.execute("DROP TABLE max_net_ads_prices;")
    op.execute("DROP TABLE max_net_ads_links;")
    op.execute("DROP TABLE max_net_ads;")
