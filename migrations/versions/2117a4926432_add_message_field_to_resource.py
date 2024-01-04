"""Add message field to resource

Revision ID: 2117a4926432
Revises: 96f3ea4d0f7a
Create Date: 2024-01-04 19:17:48.505601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2117a4926432'
down_revision = '96f3ea4d0f7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resource', schema=None) as batch_op:
        batch_op.drop_column('message')

    # ### end Alembic commands ###
