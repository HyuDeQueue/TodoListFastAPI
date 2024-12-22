"""Changing datatype for group member

Revision ID: 8de42c409139
Revises: 932321e23b4a
Create Date: 2024-12-22 15:36:51.534573

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8de42c409139'
down_revision: Union[str, None] = '932321e23b4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('group_member', 'role',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.Integer(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('group_member', 'role',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###
