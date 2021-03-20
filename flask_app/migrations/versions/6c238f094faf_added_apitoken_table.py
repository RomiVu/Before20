"""added apitoken table 

Revision ID: 6c238f094faf
Revises: 82ea8ef6cce7
Create Date: 2020-04-04 00:43:32.116264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c238f094faf'
down_revision = '82ea8ef6cce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apitoken',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=140), nullable=True),
    sa.Column('exipred', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apitoken')
    # ### end Alembic commands ###