"""empty message

Revision ID: d8f38983512a
Revises: 8b348cb5fa6c
Create Date: 2022-10-18 18:49:42.505073

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd8f38983512a'
down_revision = '8b348cb5fa6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(length=250), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=250), nullable=False))
    op.drop_index('email', table_name='user')
    op.drop_index('email_2', table_name='user')
    op.drop_column('user', 'password')
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=80), nullable=False))
    op.create_index('email_2', 'user', ['email'], unique=False)
    op.create_index('email', 'user', ['email'], unique=False)
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'name')
    # ### end Alembic commands ###
