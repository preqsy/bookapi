"""added is_deleted field in the books table

Revision ID: 6749e924d682
Revises: f37f9b6d4f5f
Create Date: 2024-01-02 11:40:42.687323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6749e924d682'
down_revision: Union[str, None] = 'f37f9b6d4f5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('is_deleted', sa.Boolean(), server_default='FALSE', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'is_deleted')
    # ### end Alembic commands ###