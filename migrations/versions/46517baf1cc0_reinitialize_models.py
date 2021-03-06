"""reinitialize models

Revision ID: 46517baf1cc0
Revises: 
Create Date: 2022-04-14 00:58:23.174541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46517baf1cc0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cursor_position',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('since_id', sa.BIGINT(), nullable=True),
    sa.Column('key_word', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=280), nullable=True),
    sa.Column('hash_tag', sa.String(length=64), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('tweet_id', sa.BIGINT(), nullable=True),
    sa.Column('score_assigned', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tweets_body'), 'tweets', ['body'], unique=False)
    op.create_index(op.f('ix_tweets_date_created'), 'tweets', ['date_created'], unique=False)
    op.create_index(op.f('ix_tweets_hash_tag'), 'tweets', ['hash_tag'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tweets_hash_tag'), table_name='tweets')
    op.drop_index(op.f('ix_tweets_date_created'), table_name='tweets')
    op.drop_index(op.f('ix_tweets_body'), table_name='tweets')
    op.drop_table('tweets')
    op.drop_table('cursor_position')
    # ### end Alembic commands ###
