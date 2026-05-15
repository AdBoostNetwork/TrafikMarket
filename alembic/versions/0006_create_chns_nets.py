"""006_create_chns_nets

Revision ID: 0006_create_chns_nets
Revises: 0005_create_tg_channels
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0006_create_chns_nets"
down_revision: Union[str, Sequence[str], None] = "0005_create_tg_channels"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE tg_chns_nets (
            net_announ_id  INTEGER NOT NULL,
            price          NUMERIC(10,2) NOT NULL,
            subs_count     INTEGER NULL,
            cover_count    NUMERIC(10,2) NULL,
            err            NUMERIC(10,2) NULL,
            profitability  NUMERIC(10,2) NULL,
            on_requests    BOOLEAN NOT NULL,
            requests_count INTEGER NULL,
            CONSTRAINT tg_chns_nets_pkey PRIMARY KEY (net_announ_id),
            CONSTRAINT tg_chns_nets_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_chns_nets_links (
            id             SERIAL NOT NULL,
            net_announ_id  INTEGER NOT NULL,
            link           TEXT NOT NULL,
            red_label      BOOLEAN NOT NULL DEFAULT FALSE,
            black_label    BOOLEAN NOT NULL DEFAULT FALSE,
            CONSTRAINT tg_chns_nets_links_pkey PRIMARY KEY (id),
            CONSTRAINT tg_chns_nets_links_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_chns_nets_topics (
            net_announ_id  INTEGER NOT NULL,
            topic_id       INTEGER NOT NULL,
            CONSTRAINT tg_chns_nets_topics_pkey PRIMARY KEY (net_announ_id, topic_id),
            CONSTRAINT tg_chns_nets_topics_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE,
            CONSTRAINT tg_chns_nets_topics_topic_id_fkey FOREIGN KEY (topic_id)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE tg_chns_nets_countries (
            net_announ_id  INTEGER NOT NULL,
            country_id     INTEGER NOT NULL,
            CONSTRAINT tg_chns_nets_countries_pkey PRIMARY KEY (net_announ_id, country_id),
            CONSTRAINT tg_chns_nets_countries_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES tg_chns_nets(net_announ_id) ON DELETE CASCADE,
            CONSTRAINT tg_chns_nets_countries_country_id_fkey FOREIGN KEY (country_id)
                REFERENCES countries(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE tg_chns_nets_countries;")
    op.execute("DROP TABLE tg_chns_nets_topics;")
    op.execute("DROP TABLE tg_chns_nets_links;")
    op.execute("DROP TABLE tg_chns_nets;")
