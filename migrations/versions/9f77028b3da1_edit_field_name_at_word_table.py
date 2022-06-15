"""edit field name at Word table

Revision ID: 9f77028b3da1
Revises: 816af45434ba
Create Date: 2022-05-25 10:27:02.132775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f77028b3da1'
down_revision = '816af45434ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('body', sa.String(length=64), nullable=True))
    op.drop_index('ix_word_word', table_name='word')
    op.create_index(op.f('ix_word_body'), 'word', ['body'], unique=False)
    op.drop_column('word', 'word')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('word', sa.Column('word', sa.VARCHAR(length=64), nullable=True))
    op.drop_index(op.f('ix_word_body'), table_name='word')
    op.create_index('ix_word_word', 'word', ['word'], unique=False)
    op.drop_column('word', 'body')
    # ### end Alembic commands ###