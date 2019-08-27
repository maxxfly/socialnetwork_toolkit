"""create post table

Revision ID: c5f401b99ad3
Revises:
Create Date: 2019-08-20 23:59:33.147285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5f401b99ad3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('key', sa.String(50), nullable=False),
        sa.Column('url', sa.String(255), nullable=False),
        sa.Column('from_network', sa.String(12), nullable=False),
        sa.Column('use_on_pinterest', sa.Boolean(), nullable=False),
        sa.Column('use_on_twitter', sa.Boolean(), nullable=False),
        sa.Column('md5', sa.String(255), nullable=False),
        sa.Column('url_target', sa.String(255), nullable=False),
        sa.Column('posted_at', sa.DateTime())
    )

def downgrade():
    op.drop_table('posts')
