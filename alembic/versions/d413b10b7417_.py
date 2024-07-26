"""empty message

Revision ID: d413b10b7417
Revises: eef26ffcaf16
Create Date: 2024-07-25 10:13:34.339912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd413b10b7417'
down_revision: Union[str, None] = 'eef26ffcaf16'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
