"""add documents_required to schemes

Revision ID: 7e09d8eee040
Revises: 311cc93b322f
Create Date: 2026-05-14 13:02:03.902402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e09d8eee040'
down_revision: Union[str, Sequence[str], None] = '311cc93b322f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'schemes',
        sa.Column('documents_required', sa.Text(), nullable=False,
                  server_default='Not specified')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('schemes', 'documents_required')