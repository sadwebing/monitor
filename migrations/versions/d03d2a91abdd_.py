"""empty message

Revision ID: d03d2a91abdd
Revises: 59d998ba1320
Create Date: 2017-02-25 12:18:19.881024

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd03d2a91abdd'
down_revision = '59d998ba1320'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('mail', 'status', existing_type=sa.String(64), type_=sa.String(20))


def downgrade():
    pass
