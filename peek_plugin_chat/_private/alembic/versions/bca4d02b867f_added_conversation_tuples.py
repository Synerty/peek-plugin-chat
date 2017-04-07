"""Added conversation tuples

Peek Plugin Database Migration Script

Revision ID: bca4d02b867f
Revises: 335064fa0821
Create Date: 2017-04-07 20:40:37.438586

"""

# revision identifiers, used by Alembic.
revision = 'bca4d02b867f'
down_revision = '335064fa0821'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
import geoalchemy2


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ConversationTuple',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hasUnreads', sa.Boolean(), nullable=False),
    sa.Column('lastActivity', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_chat'
    )
    op.create_table('ConversationUserTuple',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('convId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(length=2000), nullable=False),
    sa.Column('isUserExternal', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['convId'], ['pl_chat.ConversationTuple.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_chat'
    )
    op.create_index('idx_ConvUser_convId', 'ConversationUserTuple', ['convId'], unique=False, schema='pl_chat')
    op.create_index('idx_ConvUser_userId', 'ConversationUserTuple', ['userId'], unique=False, schema='pl_chat')
    op.create_table('MessageTuple',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('convId', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=2000), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('fromUserId', sa.String(length=40), nullable=False),
    sa.Column('dateTime', sa.DateTime(), nullable=False),
    sa.Column('state', sa.Integer(), nullable=False),
    sa.Column('onReadPayload', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['convId'], ['pl_chat.ConversationTuple.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='pl_chat'
    )
    op.create_index('idx_ChatMsgTuple_convId', 'MessageTuple', ['convId'], unique=False, schema='pl_chat')
    op.create_index('idx_ChatMsgTuple_dateTime', 'MessageTuple', ['dateTime'], unique=False, schema='pl_chat')
    op.drop_table('StringIntTuple', schema='pl_chat')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('StringIntTuple',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'pl_chat."StringIntTuple_id_seq"\'::regclass)'), nullable=False),
    sa.Column('string1', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('int1', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='StringIntTuple_pkey'),
    schema='pl_chat'
    )
    op.drop_index('idx_ChatMsgTuple_dateTime', table_name='MessageTuple', schema='pl_chat')
    op.drop_index('idx_ChatMsgTuple_convId', table_name='MessageTuple', schema='pl_chat')
    op.drop_table('MessageTuple', schema='pl_chat')
    op.drop_index('idx_ConvUser_userId', table_name='ConversationUserTuple', schema='pl_chat')
    op.drop_index('idx_ConvUser_convId', table_name='ConversationUserTuple', schema='pl_chat')
    op.drop_table('ConversationUserTuple', schema='pl_chat')
    op.drop_table('ConversationTuple', schema='pl_chat')
    # ### end Alembic commands ###