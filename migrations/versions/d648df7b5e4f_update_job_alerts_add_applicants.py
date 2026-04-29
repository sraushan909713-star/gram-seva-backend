"""update_job_alerts_add_applicants

Revision ID: d648df7b5e4f
Revises: e3258a404f92
Create Date: 2026-04-29 14:52:25.020381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd648df7b5e4f'
down_revision: Union[str, Sequence[str], None] = 'e3258a404f92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Step 1: Recreate job_alerts with correct enum ─────────
    # SQLite doesn't support ALTER COLUMN, so we drop and recreate
    op.drop_table('job_alerts')
    op.create_table(
        'job_alerts',
        sa.Column('id',           sa.String(),  nullable=False),
        sa.Column('village_id',   sa.Integer(), nullable=False),
        sa.Column('title',        sa.String(),  nullable=False),
        sa.Column('organization', sa.String(),  nullable=False),
        sa.Column('category',
            sa.Enum('government','private','railway','banking',
                    'defence','teaching','other', name='jobcategory'),
            nullable=False),
        sa.Column('total_posts',  sa.Integer(), nullable=True),
        sa.Column('eligibility',  sa.Text(),    nullable=False),
        sa.Column('how_to_apply', sa.Text(),    nullable=False),
        sa.Column('apply_link',   sa.String(),  nullable=True),
        sa.Column('last_date',    sa.Date(),    nullable=False),
        sa.Column('salary_range', sa.String(),  nullable=True),
        sa.Column('notes',        sa.Text(),    nullable=True),
        sa.Column('is_active',    sa.Boolean(), nullable=False),
        sa.Column('created_at',   sa.DateTime(timezone=True),
                  server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at',   sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # ── Step 2: Create job_applicants table ───────────────────
    op.create_table(
        'job_applicants',
        sa.Column('id',                sa.String(),  nullable=False),
        sa.Column('job_id',            sa.String(),  nullable=False),
        sa.Column('name',              sa.String(),  nullable=False),
        sa.Column('relative_name',     sa.String(),  nullable=True),
        sa.Column('gender',            sa.String(6), nullable=False),
        sa.Column('photo_url',         sa.String(),  nullable=True),
        sa.Column('gram_seva_user_id', sa.String(),  nullable=True),
        sa.Column('applied_date',      sa.Date(),    nullable=True),
        sa.Column('is_active',         sa.Boolean(), nullable=False),
        sa.Column('created_at',        sa.DateTime(timezone=True),
                  server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.ForeignKeyConstraint(['job_id'],            ['job_alerts.id']),
        sa.ForeignKeyConstraint(['gram_seva_user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('job_applicants')
    op.drop_table('job_alerts')
