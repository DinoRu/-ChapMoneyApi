"""Create all tables

Revision ID: cef4d949870f
Revises: 047eca055848
Create Date: 2024-10-26 14:02:23.899345

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cef4d949870f'
down_revision: Union[str, None] = '047eca055848'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('account_name', sa.String(), nullable=False),
    sa.Column('account_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('account_number')
    )
    op.create_index(op.f('ix_accounts_account_name'), 'accounts', ['account_name'], unique=True)
    op.create_index(op.f('ix_accounts_guid'), 'accounts', ['guid'], unique=False)
    op.create_table('currencies',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sqlalchemy_utils.types.currency.CurrencyType(length=3), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_currencies_guid'), 'currencies', ['guid'], unique=False)
    op.create_table('users',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
    sa.Column('phone', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_users_guid'), 'users', ['guid'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('conversion_rates',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('from_currency_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('to_currency_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('rates', sa.DECIMAL(precision=10, scale=3), nullable=False),
    sa.ForeignKeyConstraint(['from_currency_id'], ['currencies.guid'], ),
    sa.ForeignKeyConstraint(['to_currency_id'], ['currencies.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_conversion_rates_guid'), 'conversion_rates', ['guid'], unique=False)
    op.create_table('countries',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('calling_phone', sa.String(), nullable=False),
    sa.Column('flag_url', sa.String(), nullable=True),
    sa.Column('currency_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['currency_id'], ['currencies.guid'], ),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('calling_phone'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_countries_guid'), 'countries', ['guid'], unique=False)
    op.create_index(op.f('ix_countries_name'), 'countries', ['name'], unique=True)
    op.create_table('currency_prices',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('current_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['current_id'], ['currencies.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_currency_prices_guid'), 'currency_prices', ['guid'], unique=False)
    op.create_table('receiving_methods',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['country_id'], ['countries.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_receiving_methods_guid'), 'receiving_methods', ['guid'], unique=False)
    op.create_index(op.f('ix_receiving_methods_name'), 'receiving_methods', ['name'], unique=True)
    op.create_table('sending_methods',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('country_guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('account_guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.ForeignKeyConstraint(['account_guid'], ['accounts.guid'], ),
    sa.ForeignKeyConstraint(['country_guid'], ['countries.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_sending_methods_guid'), 'sending_methods', ['guid'], unique=False)
    op.create_index(op.f('ix_sending_methods_name'), 'sending_methods', ['name'], unique=False)
    op.create_table('transfer_fees',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('sender_country_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('receiver_country_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('fee_percentage', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['receiver_country_id'], ['countries.guid'], ),
    sa.ForeignKeyConstraint(['sender_country_id'], ['countries.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_transfer_fees_guid'), 'transfer_fees', ['guid'], unique=False)
    op.create_table('transactions',
    sa.Column('guid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('converted_amount', sa.Float(), nullable=False),
    sa.Column('final_amount', sa.Float(), nullable=False),
    sa.Column('sender_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('sending_country_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('sending_currency_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('sending_method_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('receiving_country_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('receiving_currency_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('receiving_method_id', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=False),
    sa.Column('recipient_name', sa.String(), nullable=False),
    sa.Column('recipient_phone', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20), nullable=False),
    sa.Column('transaction_status', sa.Enum('INITIATED', 'PENDING', 'COMPLETED', 'CANCELLED', name='transactionstatus'), nullable=False),
    sa.ForeignKeyConstraint(['receiving_country_id'], ['countries.guid'], ),
    sa.ForeignKeyConstraint(['receiving_currency_id'], ['currencies.guid'], ),
    sa.ForeignKeyConstraint(['receiving_method_id'], ['receiving_methods.guid'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.guid'], ),
    sa.ForeignKeyConstraint(['sending_country_id'], ['countries.guid'], ),
    sa.ForeignKeyConstraint(['sending_currency_id'], ['currencies.guid'], ),
    sa.ForeignKeyConstraint(['sending_method_id'], ['sending_methods.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_transactions_guid'), 'transactions', ['guid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_guid'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_transfer_fees_guid'), table_name='transfer_fees')
    op.drop_table('transfer_fees')
    op.drop_index(op.f('ix_sending_methods_name'), table_name='sending_methods')
    op.drop_index(op.f('ix_sending_methods_guid'), table_name='sending_methods')
    op.drop_table('sending_methods')
    op.drop_index(op.f('ix_receiving_methods_name'), table_name='receiving_methods')
    op.drop_index(op.f('ix_receiving_methods_guid'), table_name='receiving_methods')
    op.drop_table('receiving_methods')
    op.drop_index(op.f('ix_currency_prices_guid'), table_name='currency_prices')
    op.drop_table('currency_prices')
    op.drop_index(op.f('ix_countries_name'), table_name='countries')
    op.drop_index(op.f('ix_countries_guid'), table_name='countries')
    op.drop_table('countries')
    op.drop_index(op.f('ix_conversion_rates_guid'), table_name='conversion_rates')
    op.drop_table('conversion_rates')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_guid'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_currencies_guid'), table_name='currencies')
    op.drop_table('currencies')
    op.drop_index(op.f('ix_accounts_guid'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_account_name'), table_name='accounts')
    op.drop_table('accounts')
    # ### end Alembic commands ###
