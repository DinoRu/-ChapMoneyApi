"""Add time base data

Revision ID: adf91c06d3ec
Revises: cef4d949870f
Create Date: 2024-10-26 19:51:11.154743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adf91c06d3ec'
down_revision: Union[str, None] = 'cef4d949870f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('accounts', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('conversion_rates', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('conversion_rates', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('countries', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('countries', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('currencies', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('currencies', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('currency_prices', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('currency_prices', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('receiving_methods', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('receiving_methods', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('sending_methods', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('sending_methods', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transactions', sa.Column('completed_at', sa.DateTime(), nullable=True))
    op.add_column('transactions', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transactions', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transfer_fees', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('transfer_fees', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transfer_fees', 'updated_at')
    op.drop_column('transfer_fees', 'created_at')
    op.drop_column('transactions', 'updated_at')
    op.drop_column('transactions', 'created_at')
    op.drop_column('transactions', 'completed_at')
    op.drop_column('sending_methods', 'updated_at')
    op.drop_column('sending_methods', 'created_at')
    op.drop_column('receiving_methods', 'updated_at')
    op.drop_column('receiving_methods', 'created_at')
    op.drop_column('currency_prices', 'updated_at')
    op.drop_column('currency_prices', 'created_at')
    op.drop_column('currencies', 'updated_at')
    op.drop_column('currencies', 'created_at')
    op.drop_column('countries', 'updated_at')
    op.drop_column('countries', 'created_at')
    op.drop_column('conversion_rates', 'updated_at')
    op.drop_column('conversion_rates', 'created_at')
    op.drop_column('accounts', 'updated_at')
    op.drop_column('accounts', 'created_at')
    # ### end Alembic commands ###
