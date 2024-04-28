"""Init

Revision ID: 6a4794fe07e7
Revises: e4838986615e
Create Date: 2024-04-23 21:57:55.983137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a4794fe07e7'
down_revision: Union[str, None] = 'e4838986615e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('crated_at', sa.DateTime(), nullable=True),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=100), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id', 'user_id', name='unique_tag_user')
    )
    op.drop_table('Contacts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Contacts',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Contacts_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('phone', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('birthday', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Contacts_pkey')
    )
    op.drop_table('contacts')
    op.drop_table('users')
    # ### end Alembic commands ###