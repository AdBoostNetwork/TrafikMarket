"""015_create_traffic

Revision ID: 0015_create_traffic
Revises: 0014_create_stories_nets
Create Date: 2026-05-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0015_create_traffic"
down_revision: Union[str, Sequence[str], None] = "0014_create_stories_nets"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE traffic (
            traffic_id INTEGER NOT NULL,
            price      NUMERIC(10,2) NOT NULL,
            min_subs   INTEGER NOT NULL,
            max_subs   INTEGER NOT NULL,
            topic      INTEGER NOT NULL,
            country    INTEGER NOT NULL,
            platform   INTEGER NOT NULL,
            type       INTEGER NOT NULL,
            auditory   INTEGER NOT NULL,
            CONSTRAINT traffic_pkey PRIMARY KEY (traffic_id),
            CONSTRAINT traffic_traffic_id_fkey FOREIGN KEY (traffic_id)
                REFERENCES announs(announ_id) ON DELETE CASCADE,
            CONSTRAINT traffic_topic_fkey FOREIGN KEY (topic)
                REFERENCES topics(id) ON DELETE CASCADE,
            CONSTRAINT traffic_country_fkey FOREIGN KEY (country)
                REFERENCES countries(id) ON DELETE CASCADE,
            CONSTRAINT traffic_platform_fkey FOREIGN KEY (platform)
                REFERENCES platforms(id) ON DELETE CASCADE,
            CONSTRAINT traffic_type_fkey FOREIGN KEY (type)
                REFERENCES traffic_types(id) ON DELETE CASCADE,
            CONSTRAINT traffic_auditory_fkey FOREIGN KEY (auditory)
                REFERENCES audience_types(id) ON DELETE CASCADE
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE traffic;")
