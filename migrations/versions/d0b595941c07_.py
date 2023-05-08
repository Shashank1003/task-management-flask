"""empty message

Revision ID: d0b595941c07
Revises: 
Create Date: 2023-05-07 19:59:22.419786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0b595941c07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('story_points', sa.Integer(), nullable=True),
    sa.Column('reporter', sa.String(length=30), nullable=False),
    sa.Column('assignee', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('subtasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('assignee', sa.String(length=30), nullable=False),
    sa.Column('parent_task_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subtasks')
    op.drop_table('users')
    op.drop_table('tasks')
    # ### end Alembic commands ###