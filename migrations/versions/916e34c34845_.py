"""empty message

Revision ID: 916e34c34845
Revises: 6ed4914834de
Create Date: 2018-10-18 15:52:44.994720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '916e34c34845'
down_revision = '6ed4914834de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('packing', sa.Column('sorts_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'packing', 'sorts', ['sorts_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'packing', type_='foreignkey')
    op.drop_column('packing', 'sorts_id')
    # ### end Alembic commands ###
