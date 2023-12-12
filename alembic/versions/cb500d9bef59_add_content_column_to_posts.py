"""add content column to posts

Revision ID: cb500d9bef59
Revises: 5ccb59581e53
Create Date: 2023-12-09 19:54:05.669676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cb500d9bef59'
down_revision: Union[str, None] = '5ccb59581e53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
