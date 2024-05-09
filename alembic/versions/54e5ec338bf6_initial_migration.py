"""Initial migration

Revision ID: 54e5ec338bf6
Revises: 
Create Date: 2024-05-09 14:35:30.097589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54e5ec338bf6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_title'), 'achievements', ['title'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('language', sa.Enum('russian', 'english', name='language'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('user_achievement',
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('achievement', sa.Integer(), nullable=True),
    sa.Column('rewarded_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['achievement'], ['achievements.id'], ),
    sa.ForeignKeyConstraint(['user'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_achievement')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_achievements_title'), table_name='achievements')
    op.drop_table('achievements')
    # ### end Alembic commands ###