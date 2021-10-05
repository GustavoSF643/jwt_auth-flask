"""UserModel modified

Revision ID: 2ff7069e18bc
Revises: 4da78131cacc
Create Date: 2021-10-05 18:10:40.322619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ff7069e18bc'
down_revision = '4da78131cacc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'api_key')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('api_key', sa.VARCHAR(length=511), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
