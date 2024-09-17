"""empty message

Revision ID: ec709cd06e8d
Revises: 2088f5da2c59
Create Date: 2023-10-24 12:16:50.463907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec709cd06e8d'
down_revision: Union[str, None] = '2088f5da2c59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
