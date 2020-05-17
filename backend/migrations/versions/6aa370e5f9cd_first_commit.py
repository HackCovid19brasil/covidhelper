"""first commit

Revision ID: 6aa370e5f9cd
Revises: 
Create Date: 2020-05-17 15:51:08.957059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aa370e5f9cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospital',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('address', sa.String(length=140), nullable=True),
    sa.Column('uti_places', sa.Integer(), nullable=True),
    sa.Column('care_places', sa.Integer(), nullable=True),
    sa.Column('available_uti_places', sa.Integer(), nullable=True),
    sa.Column('available_care_places', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('gender', sa.String(length=32), nullable=True),
    sa.Column('access', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_index(op.f('ix_user_userid'), 'user', ['userid'], unique=True)
    op.create_table('attendance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pacient_id', sa.Integer(), nullable=True),
    sa.Column('responsible_id', sa.Integer(), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('temperature', sa.Numeric(), nullable=True),
    sa.Column('hemacias', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('hematocritos', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('hemoglobinas', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('vcm', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('hcm', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('chcm', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('rdw', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('eritoblastos', sa.Integer(), nullable=True),
    sa.Column('leucocitos', sa.Integer(), nullable=True),
    sa.Column('mielocitos', sa.Integer(), nullable=True),
    sa.Column('metamielocitos', sa.Integer(), nullable=True),
    sa.Column('bastonetes', sa.Integer(), nullable=True),
    sa.Column('segmentados', sa.Integer(), nullable=True),
    sa.Column('neutrofilos_totais', sa.Integer(), nullable=True),
    sa.Column('eosinofilos', sa.Integer(), nullable=True),
    sa.Column('basofilos', sa.Integer(), nullable=True),
    sa.Column('linfocitos', sa.Integer(), nullable=True),
    sa.Column('monocitos', sa.Integer(), nullable=True),
    sa.Column('plasmocitos', sa.Integer(), nullable=True),
    sa.Column('plaquetas', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('vmp', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('pcr', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('influenza', sa.Integer(), nullable=True),
    sa.Column('parainfluenza', sa.Integer(), nullable=True),
    sa.Column('h1n1', sa.Integer(), nullable=True),
    sa.Column('chlamidophila_plenumonae', sa.Integer(), nullable=True),
    sa.Column('rhinovirus_enterovirus', sa.Integer(), nullable=True),
    sa.Column('virus_sincicial', sa.Integer(), nullable=True),
    sa.Column('outros_coranavirus', sa.Integer(), nullable=True),
    sa.Column('outras_infeccoes_respiratorias', sa.Integer(), nullable=True),
    sa.Column('sars_cov_2_labtest_score', sa.Float(precision=10, asdecimal=2), nullable=True),
    sa.Column('sars_cov_2_labtest_pred', sa.Integer(), nullable=True),
    sa.Column('sars_cov_2_confirmation', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['pacient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['responsible_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendance_timestamp'), 'attendance', ['timestamp'], unique=False)
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospital.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'hospital_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_index(op.f('ix_attendance_timestamp'), table_name='attendance')
    op.drop_table('attendance')
    op.drop_index(op.f('ix_user_userid'), table_name='user')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_table('user')
    op.drop_table('hospital')
    # ### end Alembic commands ###
