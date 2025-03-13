"""renamed displayed_name in users

Revision ID: cc66f3f4e5eb
Revises: 0acc9dc17320
Create Date: 2025-03-13 12:08:24.824104

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cc66f3f4e5eb"
down_revision: Union[str, None] = "0acc9dc17320"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "app1_user",
        sa.Column(
            "displayed_name",
            sa.String(length=50),
            server_default="Noname",
            nullable=False,
        ),
    )
    op.drop_column("app1_user", "Displayed user name")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "app1_user",
        sa.Column(
            "Displayed user name",
            sa.VARCHAR(length=50),
            server_default=sa.text("'Noname'::character varying"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("app1_user", "displayed_name")
    # ### end Alembic commands ###
