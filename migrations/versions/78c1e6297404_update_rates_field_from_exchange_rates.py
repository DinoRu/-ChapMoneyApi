"""Update rates field from exchange rates

Revision ID: 78c1e6297404
Revises: 5f51904be260
Create Date: 2024-11-05 10:14:16.476084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78c1e6297404'
down_revision: Union[str, None] = '5f51904be260'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('conversion_rates', 'rates',
               existing_type=sa.NUMERIC(precision=10, scale=3),
               type_=sa.Float(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('conversion_rates', 'rates',
               existing_type=sa.Float(),
               type_=sa.NUMERIC(precision=10, scale=3),
               existing_nullable=False)
    # ### end Alembic commands ###
