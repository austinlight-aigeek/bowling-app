"""Initial migration

Revision ID: 1571d35e5378
Revises: 
Create Date: 2024-10-19 05:54:15.127435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1571d35e5378'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('current_frame', sa.Integer(), nullable=True),
    sa.Column('player_ids', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('frames',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('game_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rolls',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('pins_knocked', sa.Integer(), nullable=False),
    sa.Column('frame_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['frame_id'], ['frames.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rolls')
    op.drop_table('frames')
    op.drop_table('players')
    op.drop_table('games')
    # ### end Alembic commands ###