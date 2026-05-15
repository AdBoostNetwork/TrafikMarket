"""008_create_max_chns_nets

Revision ID: 0008_create_max_chns_nets
Revises: 0007_create_max_channels
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0008_create_max_chns_nets"
down_revision: Union[str, Sequence[str], None] = "0007_create_max_channels"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE max_chns_nets (
            net_announ_id  INTEGER NOT NULL,
            price          NUMERIC(10,2) NOT NULL,
            subs_count     INTEGER NULL,
            cover_count    NUMERIC(10,2) NULL,
            err            NUMERIC(10,2) NULL,
            profitability  NUMERIC(10,2) NULL,
            on_requests    BOOLEAN NOT NULL,
            requests_count INTEGER NULL,
            CONSTRAINT max_chns_nets_pkey PRIMARY KEY (net_announ_id),
            CONSTRAINT max_chns_nets_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_chns_nets_links (
            id             SERIAL NOT NULL,
            net_announ_id  INTEGER NOT NULL,
            link           TEXT NOT NULL,
            CONSTRAINT max_chns_nets_links_pkey PRIMARY KEY (id),
            CONSTRAINT max_chns_nets_links_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES max_chns_nets(net_announ_id) ON DELETE CASCADE
        );
        """
    )

    op.execute(
        """
        CREATE TABLE max_chns_nets_topics (
            net_announ_id  INTEGER NOT NULL,
            topic_id       INTEGER NOT NULL,
            CONSTRAINT max_chns_nets_topics_pkey PRIMARY KEY (net_announ_id, topic_id),
            CONSTRAINT max_chns_nets_topics_net_announ_id_fkey FOREIGN KEY (net_announ_id)
                REFERENCES max_chns_nets(net_announ_id) ON DELETE CASCADE,
            CONSTRAINT max_chns_nets_topics_topic_id_fkey FOREIGN KEY (topic_id)
                REFERENCES topics(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE max_chns_nets_topics;")
    op.execute("DROP TABLE max_chns_nets_links;")
    op.execute("DROP TABLE max_chns_nets;")
