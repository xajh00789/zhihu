"""empty message

Revision ID: 21556f91f587
Revises: 5a61700a13a0
Create Date: 2018-04-21 16:02:54.912423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21556f91f587'
down_revision = '5a61700a13a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_title', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question')
    # ### end Alembic commands ###
