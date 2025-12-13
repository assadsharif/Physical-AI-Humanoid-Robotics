"""Create user_profiles table

Revision ID: 002
Revises: 001
Create Date: 2025-12-14 12:00:00.000000

This migration creates the user_profiles table for application-specific
user profile data (experience level, preferences).
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create user_profiles table"""

    op.create_table(
        'user_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, unique=True),
        sa.Column('experience_level', sa.String(20), nullable=False, server_default='beginner'),
        sa.Column('preferences', postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),

        # Foreign key to users table
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),

        # Check constraint for experience_level
        sa.CheckConstraint(
            "experience_level IN ('beginner', 'intermediate', 'advanced')",
            name='valid_experience_level'
        ),
    )

    # Create indexes
    op.create_index('user_profiles_user_id_idx', 'user_profiles', ['user_id'])
    op.create_index('user_profiles_experience_level_idx', 'user_profiles', ['experience_level'])

    # Create trigger for updating updated_at timestamp
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER update_user_profiles_updated_at
        BEFORE UPDATE ON user_profiles
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Drop user_profiles table"""

    # Drop trigger and function
    op.execute("DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")

    # Drop table (indexes drop automatically)
    op.drop_table('user_profiles')
