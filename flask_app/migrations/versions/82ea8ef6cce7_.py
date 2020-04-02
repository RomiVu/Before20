"""empty message

Revision ID: 82ea8ef6cce7
Revises: fc3f3b3d437e
Create Date: 2020-04-03 01:07:07.942782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82ea8ef6cce7'
down_revision = 'fc3f3b3d437e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('avator', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('role', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    op.drop_column('user', 'avator')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
