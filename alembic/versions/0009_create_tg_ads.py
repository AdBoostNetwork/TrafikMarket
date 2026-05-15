"""009_create_tg_ads

Revision ID: 0009_create_tg_ads
Revises: 0008_create_max_chns_nets
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0009_create_tg_ads"
down_revision: Union[str, Sequence[str], None] = "0008_create_max_chns_nets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE tg_ads (
            ad_id        INTEGER NOT NULL,
            link         TEXT NOT NULL,
            topic        INTEGER NOT NULL,
            country      INTEGER NOT NULL,
            subs_count   INTEGER NOT NULL,
            cover_count  NUMERIC(10,2) NOT NULL,
            err          NUMERIC(10,2) NULL,
            red_label    BOOLEAN NOT NULL DEFAULT FALSE,
            black_label  BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT tg_ads_pkey PRIMARY KEY (ad_id),
            CONSTRAINT tg_ads_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE,
            CONSTRAINT tg_ads_topic_fkey FOREIGN KEY (topic)
                REFERENCES topics(id) ON DELETE CASCADE,
            CONSTRAINT tg_ads_country_fkey FOREIGN KEY (country)
                REFERENCES countries(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_ads_prices (
            id     SERIAL NOT NULL,
            ad_id  INTEGER NOT NULL,
            format TEXT NOT NULL,
            price  NUMERIC(10,2) NOT NULL,
            CONSTRAINT tg_ads_prices_pkey PRIMARY KEY (id),
            CONSTRAINT tg_ads_prices_ad_id_fkey FOREIGN KEY (ad_id)
                REFERENCES tg_ads(ad_id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE tg_ads_prices;")
    op.execute("DROP TABLE tg_ads;")
