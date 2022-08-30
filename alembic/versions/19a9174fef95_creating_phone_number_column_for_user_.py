"""creating phone number column for user table

Revision ID: 19a9174fef95
Revises: 
Create Date: 2022-08-30 11:24:42.140738

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '19a9174fef95'
down_revision = None
branch_labels = None
depends_on = None


# in order to initialize alembic for your project
# use: alembic init <your folder-name goes here> command


# in order to create a revision, use:
# alembic revision -m <your message goes here> command


# in order to run upgrade, use:
# alembic upgrade <revision string>

def upgrade() -> None:
    op.add_column('user', sa.Column('phone_number', sa.String(), nullable=True))


# in order to run downgrade :
# if downgrade in not None, use: alembic downgrade -1 command
# if downgrade is initialized, use: alembic downgrade <downgrade string>
def downgrade() -> None:
    op.drop_column('user', 'phone_number')
