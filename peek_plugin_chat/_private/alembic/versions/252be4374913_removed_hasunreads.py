"""Removed hasUnreads

Peek Plugin Database Migration Script

Revision ID: 252be4374913
Revises: 5288d02e94e4
Create Date: 2017-04-09 14:28:47.090026

"""

# revision identifiers, used by Alembic.
revision = '252be4374913'
down_revision = '5288d02e94e4'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ChatUserTuple', 'hasUnreads', schema='pl_chat')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ChatUserTuple', sa.Column('hasUnreads', sa.BOOLEAN(), autoincrement=False, nullable=False), schema='pl_chat')
    # ### end Alembic commands ###