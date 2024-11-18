"""Create tables 1

Revision ID: 047eca055848
Revises: b008c6951891
Create Date: 2024-10-26 13:58:13.453184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '047eca055848'
down_revision: Union[str, None] = 'b008c6951891'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
