"""added token column to the users table and blog post column to the POst table

Revision ID: c826fbd364d7
Revises: 88b8cc1147fb
Create Date: 2025-01-15 12:23:52.172814

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c826fbd364d7'
down_revision = '88b8cc1147fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blog_post', sa.String(length=5000), nullable=True))
        batch_op.create_index(batch_op.f('ix_post_blog_post'), ['blog_post'], unique=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_blog_post'))
        batch_op.drop_column('blog_post')

    # ### end Alembic commands ###
