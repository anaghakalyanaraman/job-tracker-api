"""add jobs table

Revision ID: 624af25e7c9f
Revises: e97f7d5f9171
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '624af25e7c9f'
down_revision: Union[str, Sequence[str], None] = 'e97f7d5f9171'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table('jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('company', sa.String(length=100), nullable=False),
        sa.Column('role', sa.String(length=100), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('applied_date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('jobs')
