"""add table

Revision ID: 076b289bdd2d
Revises:
Create Date: 2024-04-01 02:07:33.452058

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "076b289bdd2d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("status_closed", sa.Boolean(), nullable=False),
        sa.Column("shift_task_representation", sa.String(), nullable=False),
        sa.Column("line", sa.String(), nullable=False),
        sa.Column("shift", sa.String(), nullable=False),
        sa.Column("brigade", sa.String(), nullable=False),
        sa.Column("batch_number", sa.Integer(), nullable=False),
        sa.Column("batch_date", sa.Date(), nullable=False),
        sa.Column("nomenclature", sa.String(), nullable=False),
        sa.Column("code_ekn", sa.String(), nullable=False),
        sa.Column("identifier_rc", sa.String(), nullable=False),
        sa.Column("shift_start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("shift_end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "batch_number", "batch_date", name="_unique_batch_number_date"
        ),
    )
    op.create_table(
        "cubes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_code", sa.String(), nullable=False),
        sa.Column("is_aggregated", sa.Boolean(), nullable=False),
        sa.Column("aggregated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_code"),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_code", sa.String(), nullable=False),
        sa.Column("is_aggregated", sa.Boolean(), nullable=False),
        sa.Column("aggregated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("task_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_code"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("products")
    op.drop_table("cubes")
    op.drop_table("tasks")
    # ### end Alembic commands ###
