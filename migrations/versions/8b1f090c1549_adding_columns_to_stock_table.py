"""Adding columns to Stock table

Revision ID: 8b1f090c1549
Revises: 
Create Date: 2024-08-07 18:01:36.879690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b1f090c1549'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Float(), nullable=False))
        batch_op.add_column(sa.Column('average_price', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.drop_column('average_price')
        batch_op.drop_column('quantity')

    # ### end Alembic commands ###
