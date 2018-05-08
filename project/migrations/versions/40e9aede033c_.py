"""empty message

Revision ID: 40e9aede033c
Revises: 7da9a8935913
Create Date: 2018-04-20 16:40:39.041542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40e9aede033c'
down_revision = '7da9a8935913'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('job', sa.String(length=20), nullable=True))
    op.add_column('user', sa.Column('liveplace', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('self_introduce', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('xueli', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'xueli')
    op.drop_column('user', 'sex')
    op.drop_column('user', 'self_introduce')
    op.drop_column('user', 'liveplace')
    op.drop_column('user', 'job')
    # ### end Alembic commands ###