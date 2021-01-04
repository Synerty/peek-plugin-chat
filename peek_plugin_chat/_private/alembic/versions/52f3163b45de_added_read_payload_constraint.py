"""Added read payload constraint

Peek Plugin Database Migration Script

Revision ID: 52f3163b45de
Revises: a4d6b26d39b7
Create Date: 2018-01-27 11:25:04.436708

"""

# revision identifiers, used by Alembic.
revision = "52f3163b45de"
down_revision = "a4d6b26d39b7"
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "MessageReadPayloadTuple_chatUserId_fkey",
        "MessageReadPayloadTuple",
        schema="pl_chat",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "MessageReadPayloadTuple",
        "ChatUserTuple",
        ["chatUserId"],
        ["id"],
        source_schema="pl_chat",
        referent_schema="pl_chat",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        None, "MessageReadPayloadTuple", schema="pl_chat", type_="foreignkey"
    )
    op.create_foreign_key(
        "MessageReadPayloadTuple_chatUserId_fkey",
        "MessageReadPayloadTuple",
        "ChatUserTuple",
        ["chatUserId"],
        ["id"],
        source_schema="pl_chat",
        referent_schema="pl_chat",
    )
    # ### end Alembic commands ###
