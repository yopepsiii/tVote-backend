"""init

Revision ID: ee275ab37e62
Revises: 
Create Date: 2024-08-25 19:41:57.588341

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ee275ab37e62"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Candidates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("year_of_study", sa.Integer(), nullable=False),
        sa.Column("group", sa.String(), nullable=False),
        sa.Column("faculty", sa.String(), nullable=False),
        sa.Column("study_dirrection", sa.String(), nullable=False),
        sa.Column("photo", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Users",
        sa.Column(
            "id", sa.Uuid(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "Admins",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["Users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "Votes",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["candidate_id"], ["Candidates.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["Users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "candidate_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("Votes")
    op.drop_table("Admins")
    op.drop_table("Users")
    op.drop_table("Candidates")
    # ### end Alembic commands ###
