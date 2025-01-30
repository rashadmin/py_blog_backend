"""added conversation

Revision ID: 7eaebaf429a0
Revises: 90cb3e14f16d
Create Date: 2025-01-30 16:01:22.444595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7eaebaf429a0'
down_revision = '90cb3e14f16d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chat_session', sa.String(length=5000), nullable=True))
        batch_op.create_index(batch_op.f('ix_post_chat_session'), ['chat_session'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_chat_session'))
        batch_op.drop_column('chat_session')

    # ### end Alembic commands ###
