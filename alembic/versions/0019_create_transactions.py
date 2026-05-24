"""019_create_transactions

Revision ID: 0019_create_transactions
Revises: 0018_create_news
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0019_create_transactions"
down_revision: Union[str, Sequence[str], None] = "0018_create_news"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        CREATE TABLE transactions_io (
            id         SERIAL NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            user_id    BIGINT NOT NULL,
            amount     NUMERIC(10,2) NOT NULL,
            type       TEXT NOT NULL,
            CONSTRAINT transactions_io_pkey PRIMARY KEY (id),
            CONSTRAINT transactions_io_user_id_fkey FOREIGN KEY (user_id)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT transactions_io_type_check CHECK (type IN ('in', 'out'))
        );
        """
    )

    op.execute(
        """
        CREATE TABLE transactions_deals (
            id         SERIAL NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            user_from  BIGINT NOT NULL,
            user_to    BIGINT NOT NULL,
            deal_id    INTEGER NOT NULL,
            announ_type TEXT NOT NULL,
            amount     NUMERIC(10,2) NOT NULL,
            type       TEXT NOT NULL,
            CONSTRAINT transactions_deals_pkey PRIMARY KEY (id),
            CONSTRAINT transactions_deals_user_from_fkey FOREIGN KEY (user_from)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT transactions_deals_user_to_fkey FOREIGN KEY (user_to)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT transactions_deals_type_check CHECK (type IN ('deal', 'fee'))
        );
        """
    )

    op.execute(
        """
        CREATE TABLE transactions_refs (
            id          SERIAL NOT NULL,
            created_at  TIMESTAMP WITH TIME ZONE NOT NULL,
            user_to     BIGINT NOT NULL,
            user_from   BIGINT NOT NULL,
            trn_deal_id INTEGER NOT NULL,
            amount      NUMERIC(10,2) NOT NULL,
            CONSTRAINT transactions_refs_pkey PRIMARY KEY (id),
            CONSTRAINT transactions_refs_user_to_fkey FOREIGN KEY (user_to)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT transactions_refs_user_from_fkey FOREIGN KEY (user_from)
                REFERENCES users(user_id) ON DELETE RESTRICT,
            CONSTRAINT transactions_refs_trn_deal_id_fkey FOREIGN KEY (trn_deal_id)
                REFERENCES transactions_deals(id) ON DELETE RESTRICT
        );
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE transactions_refs;")
    op.execute("DROP TABLE transactions_deals;")
    op.execute("DROP TABLE transactions_io;")
