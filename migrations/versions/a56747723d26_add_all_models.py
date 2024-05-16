"""add all models

Revision ID: a56747723d26
Revises: a5e196f977bf
Create Date: 2024-03-31 23:45:56.407334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a56747723d26'
down_revision = 'a5e196f977bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendence', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
