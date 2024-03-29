"""added word table

Revision ID: 816af45434ba
Revises: 7684b56a5851
Create Date: 2022-05-25 10:03:46.373447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '816af45434ba'
down_revision = '7684b56a5851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('word',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('word', sa.String(length=64), nullable=True),
    sa.Column('mask', sa.String(length=64), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_word_mask'), 'word', ['mask'], unique=False)
    op.create_index(op.f('ix_word_timestamp'), 'word', ['timestamp'], unique=False)
    op.create_index(op.f('ix_word_word'), 'word', ['word'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_word_word'), table_name='word')
    op.drop_index(op.f('ix_word_timestamp'), table_name='word')
    op.drop_index(op.f('ix_word_mask'), table_name='word')
    op.drop_table('word')
    # ### end Alembic commands ###
