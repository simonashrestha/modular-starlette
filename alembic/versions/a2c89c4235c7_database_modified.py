"""Database modified

Revision ID: a2c89c4235c7
Revises: 622d2ed35a27
Create Date: 2024-07-25 10:40:12.430759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2c89c4235c7'
down_revision: Union[str, None] = '622d2ed35a27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('image_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('blog_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('image_path', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.blog_id'], name='images_blog_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('image_id', name='images_pkey')
    )
    # ### end Alembic commands ###