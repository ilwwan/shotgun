"""First migration

Revision ID: 0ad57c240d77
Revises: 
Create Date: 2021-10-02 17:42:00.824587

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0ad57c240d77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pgbench_tellers')
    op.drop_table('pgbench_branches')
    op.drop_table('pgbench_accounts')
    op.drop_table('pgbench_history')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pgbench_history',
    sa.Column('tid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('aid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('delta', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('mtime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('filler', sa.CHAR(length=22), autoincrement=False, nullable=True)
    )
    op.create_table('pgbench_accounts',
    sa.Column('aid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('abalance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('filler', sa.CHAR(length=84), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('aid', name='pgbench_accounts_pkey')
    )
    op.create_table('pgbench_branches',
    sa.Column('bid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bbalance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('filler', sa.CHAR(length=88), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('bid', name='pgbench_branches_pkey')
    )
    op.create_table('pgbench_tellers',
    sa.Column('tid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('tbalance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('filler', sa.CHAR(length=84), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('tid', name='pgbench_tellers_pkey')
    )
    # ### end Alembic commands ###
