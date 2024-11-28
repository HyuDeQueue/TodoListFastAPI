"""Removing wrong role location

Revision ID: ed2536d32a55
Revises: 7d77f955e52e
Create Date: 2024-11-28 21:17:43.648521

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ed2536d32a55'
down_revision: Union[str, None] = '7d77f955e52e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('role', mysql.VARCHAR(length=255), nullable=False))
    # ### end Alembic commands ###
