"""create tables

Revision ID: 41325a40b08e
Revises: 
Create Date: 2024-10-20 21:02:32.780522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "41325a40b08e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player", sa.String(), nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_games_id"), "games", ["id"], unique=False)
    op.create_table(
        "frames",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("frame_number", sa.Integer(), nullable=False),
        sa.Column("rolls", postgresql.ARRAY(sa.Integer()), nullable=False),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_frames_id"), "frames", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_frames_id"), table_name="frames")
    op.drop_table("frames")
    op.drop_index(op.f("ix_games_id"), table_name="games")
    op.drop_table("games")
    # ### end Alembic commands ###
