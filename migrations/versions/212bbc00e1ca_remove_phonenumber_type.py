"""Remove phonenumber type.

Revision ID: 212bbc00e1ca
Revises: a1be3e0b28a9
Create Date: 2024-11-13 21:46:59.719260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '212bbc00e1ca'
down_revision: Union[str, None] = 'a1be3e0b28a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
