# Database Migrations

## Overview
This directory contains all database migration files for the Cash Flow Management System.

## File Structure
- `001_create_database_schema.sql` - Main database schema creation
- `002_add_indexes.sql` - Additional indexes for performance
- `003_seed_data.sql` - Initial seed data
- `rollback/` - Rollback scripts for each migration

## How to Run Migrations

### Using psql
```bash
# Connect to database
psql -h 140.245.50.242 -p 5432 -U cash_flow_user -d cash_flow_db

# Run migration
\i migrations/001_create_database_schema.sql
```

### Using Flask-Migrate
```bash
# Initialize migrations (if not already done)
flask db init

# Create migration
flask db migrate -m "Create database schema"

# Apply migration
flask db upgrade
```

## Migration Files Naming Convention
- Format: `XXX_description.sql`
- XXX: Sequential number (001, 002, 003...)
- description: Brief description of what the migration does

## Rollback
Each migration has a corresponding rollback script in the `rollback/` directory:
```bash
\i migrations/rollback/001_rollback_create_database_schema.sql
```

## Important Notes
- Always backup database before running migrations
- Test migrations on development environment first
- Use transactions in migration scripts
- Add proper error handling
- Document any breaking changes

## Database Schema
The database consists of the following modules:
- **sys**: System tables (application, history)
- **auth**: Authentication and authorization
- **tran**: Transactions and financial data
- **my_**: Personal finance management
- **com**: Common/configuration data

## Production Considerations
- All tables use `BIGSERIAL` for primary keys
- Proper indexes for performance optimization
- Soft delete with `is_deleted` flag
- Audit columns: `created_at`, `updated_at`, `created_by_user_id`, `updated_by_user_id`
- UTF-8 encoding
- UTC timezone
- Automatic timestamp updates via triggers
