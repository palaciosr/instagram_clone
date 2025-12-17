"""add file_name and image_data to posts

Revision ID: 28ba62c6170d
Revises: 53fafa60a4d7
Create Date: 2025-12-08 13:50:47.954191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ba62c6170d'
down_revision: Union[str, Sequence[str], None] = '53fafa60a4d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('posts', sa.Column('file_name', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('image_data', sa.LargeBinary(), nullable=True))

def downgrade() -> None:
    op.drop_column('posts', 'image_data')
    op.drop_column('posts', 'file_name')
