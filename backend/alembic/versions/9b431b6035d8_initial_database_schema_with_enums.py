"""Initial database schema with enums

Revision ID: xxxxx
Revises:
Create Date: 2025-xx-xx xx:xx:xx.xxxxxx

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'xxxxx'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create ENUM types first
    usertype_enum = postgresql.ENUM('recruiter', 'job_seeker', name='usertype')
    usertype_enum.create(op.get_bind(), checkfirst=True)

    applicationstatus_enum = postgresql.ENUM('pending', 'reviewed', 'accepted', 'rejected', name='applicationstatus')
    applicationstatus_enum.create(op.get_bind(), checkfirst=True)

    # Now create tables
    op.create_table('users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('user_type', postgresql.ENUM('recruiter', 'job_seeker', name='usertype', create_type=False), nullable=False),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)

    op.create_table('skills',
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(), nullable=False),
        sa.Column('skill_type', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('skill_id')
    )
    op.create_index(op.f('ix_skills_skill_id'), 'skills', ['skill_id'], unique=False)
    op.create_index(op.f('ix_skills_skill_name'), 'skills', ['skill_name'], unique=True)

    op.create_table('job_seekers',
        sa.Column('seeker_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('seeker_id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_job_seekers_seeker_id'), 'job_seekers', ['seeker_id'], unique=False)

    op.create_table('recruiters',
        sa.Column('recruiter_id', sa.Integer(), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('company_description', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('recruiter_id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_recruiters_recruiter_id'), 'recruiters', ['recruiter_id'], unique=False)

    op.create_table('jobs',
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('job_title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('recruiter_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['recruiter_id'], ['recruiters.recruiter_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('job_id')
    )
    op.create_index(op.f('ix_jobs_job_id'), 'jobs', ['job_id'], unique=False)
    op.create_index(op.f('ix_jobs_job_title'), 'jobs', ['job_title'], unique=False)

    op.create_table('resumes',
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('seeker_id', sa.Integer(), nullable=False),
        sa.Column('about_me', sa.Text(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['seeker_id'], ['job_seekers.seeker_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('resume_id')
    )
    op.create_index(op.f('ix_resumes_resume_id'), 'resumes', ['resume_id'], unique=False)

    op.create_table('applications',
        sa.Column('application_id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('seeker_id', sa.Integer(), nullable=False),
        sa.Column('application_date', sa.Date(), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'reviewed', 'accepted', 'rejected', name='applicationstatus', create_type=False), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.job_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['seeker_id'], ['job_seekers.seeker_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('application_id')
    )
    op.create_index(op.f('ix_applications_application_id'), 'applications', ['application_id'], unique=False)

    op.create_table('certifications',
        sa.Column('cert_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('cert_name', sa.String(), nullable=False),
        sa.Column('issuing_organization', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.resume_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('cert_id')
    )
    op.create_index(op.f('ix_certifications_cert_id'), 'certifications', ['cert_id'], unique=False)

    op.create_table('educations',
        sa.Column('education_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('school_name', sa.String(), nullable=False),
        sa.Column('degree', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.resume_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('education_id')
    )
    op.create_index(op.f('ix_educations_education_id'), 'educations', ['education_id'], unique=False)

    op.create_table('resume_skills',
        sa.Column('resume_skill_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.resume_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.skill_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('resume_skill_id')
    )
    op.create_index(op.f('ix_resume_skills_resume_skill_id'), 'resume_skills', ['resume_skill_id'], unique=False)

    # Add foreign key for job_seekers.resume_id after resumes table is created
    op.create_foreign_key('fk_job_seekers_resume_id', 'job_seekers', 'resumes', ['resume_id'], ['resume_id'], ondelete='SET NULL')


def downgrade():
    op.drop_constraint('fk_job_seekers_resume_id', 'job_seekers', type_='foreignkey')
    op.drop_table('resume_skills')
    op.drop_table('educations')
    op.drop_table('certifications')
    op.drop_table('applications')
    op.drop_table('resumes')
    op.drop_table('jobs')
    op.drop_table('recruiters')
    op.drop_table('job_seekers')
    op.drop_table('skills')
    op.drop_table('users')

    # Drop ENUM types
    postgresql.ENUM(name='applicationstatus').drop(op.get_bind())
    postgresql.ENUM(name='usertype').drop(op.get_bind())
