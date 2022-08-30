"""create address_id in user table ad Foreign Key

Revision ID: 361bc3ccd8b9
Revises: 54dfea9daf05
Create Date: 2022-08-30 12:20:10.829815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '361bc3ccd8b9'
down_revision = '54dfea9daf05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_user_fk',
                          source_table='user',
                          referent_table='address',
                          local_cols=['address_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_user_fk', table_name='user')
    op.drop_column('user', column_name='address_id')
