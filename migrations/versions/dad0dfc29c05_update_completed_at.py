"""Update completed_at.

Revision ID: dad0dfc29c05
Revises: 212bbc00e1ca
Create Date: 2024-11-13 22:55:56.577125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dad0dfc29c05'
down_revision: Union[str, None] = '212bbc00e1ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'completed_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('transactions', 'completed_at',
               existing_type=sa.String(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    # ### end Alembic commands ###
