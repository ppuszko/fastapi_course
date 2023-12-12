"""add foreign key to posts table

Revision ID: 417c122c5e7c
Revises: 435b1a504db8
Create Date: 2023-12-09 20:10:40.638126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '417c122c5e7c'
down_revision: Union[str, None] = '435b1a504db8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table="posts", referent_table="users", 
                         local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    
    pass
