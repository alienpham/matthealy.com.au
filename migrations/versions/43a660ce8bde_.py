"""empty message

Revision ID: 43a660ce8bde
Revises: 16f851bde1cc
Create Date: 2015-04-07 15:10:42.615973

"""

# revision identifiers, used by Alembic.
revision = '43a660ce8bde'
down_revision = '16f851bde1cc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('content_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'content_html')
    ### end Alembic commands ###
