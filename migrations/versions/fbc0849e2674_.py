"""merge mozilla updates with schema from master

Revision ID: fbc0849e2674
Revises: 6b5be7e0a0ef, 7671dca4e604
Create Date: 2017-12-12 04:45:34.360587

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'fbc0849e2674'
down_revision = ('6b5be7e0a0ef', '7671dca4e604')
branch_labels = None
depends_on = None


def upgrade():
    # Upstream changed the column name in migration revision 7671dca4e604 --
    # see git revision 62e5e3892603502c5f3a6da277c33c73510b8819
    op.alter_column('users', 'image_url', new_column_name='profile_image_url')

    pass


def downgrade():
    pass
