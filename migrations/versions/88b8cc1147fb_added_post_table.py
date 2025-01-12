"""added post table

Revision ID: 88b8cc1147fb
Revises: 00f7e50cfdd2
Create Date: 2025-01-12 18:14:30.650473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88b8cc1147fb'
down_revision = '00f7e50cfdd2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.String(length=64), nullable=True),
    sa.Column('original_post', sa.String(length=5000), nullable=True),
    sa.Column('linkedin_post', sa.String(length=5000), nullable=True),
    sa.Column('facebook_post', sa.String(length=5000), nullable=True),
    sa.Column('twitter_thread', sa.String(length=5000), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('facebook_post'),
    sa.UniqueConstraint('linkedin_post'),
    sa.UniqueConstraint('twitter_thread')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_original_post'), ['original_post'], unique=True)
        batch_op.create_index(batch_op.f('ix_post_post_id'), ['post_id'], unique=True)
        batch_op.create_index(batch_op.f('ix_post_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_timestamp'))
        batch_op.drop_index(batch_op.f('ix_post_post_id'))
        batch_op.drop_index(batch_op.f('ix_post_original_post'))

    op.drop_table('post')
    # ### end Alembic commands ###