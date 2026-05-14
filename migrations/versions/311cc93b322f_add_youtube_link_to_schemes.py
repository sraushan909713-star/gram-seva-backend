"""add youtube_link to schemes

Revision ID: 311cc93b322f
Revises: 4538f4acc9b0
Create Date: 2026-05-14 02:04:27.536545

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '311cc93b322f'
down_revision: Union[str, Sequence[str], None] = '4538f4acc9b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('schemes', sa.Column('youtube_link', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('schemes', 'youtube_link')