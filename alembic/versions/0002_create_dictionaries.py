"""002_create_dictionaries

Revision ID: 0002_create_dictionaries
Revises: 2e48773d7daf
Create Date: 2026-05-14 14:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0002_create_dictionaries"
down_revision: Union[str, Sequence[str], None] = "2e48773d7daf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE countries (
            id SERIAL NOT NULL,
            country_name TEXT NOT NULL,
            CONSTRAINT countries_pkey PRIMARY KEY (id),
            CONSTRAINT countries_country_name_key UNIQUE (country_name)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE topics (
            id SERIAL NOT NULL,
            topic_name TEXT NOT NULL,
            CONSTRAINT topics_pkey PRIMARY KEY (id),
            CONSTRAINT topics_topic_name_key UNIQUE (topic_name)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE platforms (
            id SERIAL NOT NULL,
            platform_name TEXT NOT NULL,
            CONSTRAINT platforms_pkey PRIMARY KEY (id),
            CONSTRAINT platforms_platform_name_key UNIQUE (platform_name)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE traffic_types (
            id SERIAL NOT NULL,
            traffic_type_name TEXT NOT NULL,
            CONSTRAINT traffic_types_pkey PRIMARY KEY (id),
            CONSTRAINT traffic_types_traffic_type_name_key UNIQUE (traffic_type_name)
        );
        """
    )

    op.execute(
        """
        CREATE TABLE audience_types (
            id SERIAL NOT NULL,
            type_name TEXT NOT NULL,
            CONSTRAINT audience_types_pkey PRIMARY KEY (id),
            CONSTRAINT audience_types_type_name_key UNIQUE (type_name)
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE audience_types;")
    op.execute("DROP TABLE traffic_types;")
    op.execute("DROP TABLE platforms;")
    op.execute("DROP TABLE topics;")
    op.execute("DROP TABLE countries;")
