"""011_create_max_ads

Revision ID: 0011_create_max_ads
Revises: 0010_create_tg_net_ads
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0011_create_max_ads"
down_revision: Union[str, Sequence[str], None] = "0010_create_tg_net_ads"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE max_ads (
            ad_id        INTEGER NOT NULL,
            link         TEXT NOT NULL,
            topic        INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            CONSTRAINT max_ads_pkey PRIMARY KEY (ad_id),
            CONSTRAINT max_ads_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE,
            CONSTRAINT max_ads_topic_fkey FOREIGN KEY (topic)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_ads_prices (
            id     SERIAL NOT NULL,
            ad_id  INTEGER NOT NULL,
            format TEXT NOT NULL,
            price  NUMERIC(10,2) NOT NULL,
            CONSTRAINT max_ads_prices_pkey PRIMARY KEY (id),
            CONSTRAINT max_ads_prices_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES max_ads(ad_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE max_ads_prices;")
    op.execute("DROP TABLE max_ads;")
