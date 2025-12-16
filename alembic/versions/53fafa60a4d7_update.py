"""update

Revision ID: 53fafa60a4d7
Revises: 
Create Date: 2025-12-08 11:31:17.727056

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '53fafa60a4d7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('file_name', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('image_data', sa.LargeBinary(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # ##
    op.drop_column('posts', 'image_data')
    op.drop_column('posts', 'file_name')

    