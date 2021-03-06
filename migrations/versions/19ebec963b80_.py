"""empty message

Revision ID: 19ebec963b80
Revises: 49c3959e4949
Create Date: 2017-02-27 23:38:12.158766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19ebec963b80'
down_revision = '49c3959e4949'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tomcat_project', sa.Column('code_dir', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tomcat_project', 'code_dir')
    # ### end Alembic commands ###
