"""Create better-auth tables for authentication

Revision ID: 001
Revises:
Create Date: 2025-12-14 00:00:00.000000

This migration creates the base schema required by better-auth:
- users: User account information
- accounts: Authentication provider accounts (password, OAuth, etc)
- sessions: User sessions for authentication
- verification: Email verification tokens and codes
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create better-auth schema"""

    # Create UUID type if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('email_verified', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('image', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('users_email_idx', 'users', ['email'])

    # accounts table
    op.create_table(
        'accounts',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('account_id', sa.String(255), nullable=False),
        sa.Column('provider_id', sa.String(50), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('id_token', sa.Text(), nullable=True),
        sa.Column('access_token_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('refresh_token_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('scope', sa.String(1000), nullable=True),
        sa.Column('password', sa.Text(), nullable=True),  # For credential provider
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('provider_id', 'account_id', name='accounts_provider_account_unique'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('accounts_user_id_idx', 'accounts', ['user_id'])
    op.create_index('accounts_provider_id_idx', 'accounts', ['provider_id'])

    # sessions table
    op.create_table(
        'sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('token', sa.Text(), unique=True, nullable=False),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('user_agent', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('sessions_user_id_idx', 'sessions', ['user_id'])
    op.create_index('sessions_token_idx', 'sessions', ['token'])
    op.create_index('sessions_expires_at_idx', 'sessions', ['expires_at'])

    # verification table (for email verification, password reset, etc)
    op.create_table(
        'verification',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), primary_key=True),
        sa.Column('identifier', sa.String(255), nullable=False),  # Email address for verification
        sa.Column('value', sa.String(500), nullable=False),  # Verification code
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('identifier', 'value', name='verification_identifier_value_unique'),
    )
    op.create_index('verification_identifier_idx', 'verification', ['identifier'])
    op.create_index('verification_expires_at_idx', 'verification', ['expires_at'])


def downgrade() -> None:
    """Drop better-auth schema"""

    # Drop tables in reverse order of creation (due to foreign keys)
    op.drop_table('verification')
    op.drop_table('sessions')
    op.drop_table('accounts')
    op.drop_table('users')
