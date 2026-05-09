# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** database running
3. **Git** for cloning repository

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd service-cash-flow
```

### 2. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Or install psycopg2-binary if needed
pip install psycopg2-binary
```

### 3. Database Setup

#### Option A: Using SSH Tunnel (Recommended)

```bash
# Create SSH tunnel to PostgreSQL server
ssh -N -L 5432:localhost:5432 cash_flow_service@140.245.50.242

# Keep this terminal open and run in another terminal
```

#### Option B: Local PostgreSQL

```bash
# Create database
createdb cash_flow_db

# Create user
psql -d cash_flow_db -c "CREATE USER cash_flow_user WITH PASSWORD 'Minhduc24022@1';"
psql -d cash_flow_db -c "GRANT ALL PRIVILEGES ON DATABASE cash_flow_db TO cash_flow_user;"
```

### 4. Configure Environment

Copy and edit the `.env` file:

```bash
# For SSH tunnel (localhost connection)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cash_flow_db
DB_USER=cash_flow_user
DB_PASSWORD=Minhduc24022@1

# For direct server connection
# DB_HOST=140.245.50.242
# DB_PORT=5432
```

### 5. Run Database Migrations

```bash
# Run main schema migration
psql -h localhost -p 5432 -U cash_flow_user -d cash_flow_db -f migrations/001_create_database_schema.sql

# Run token field length fix
psql -h localhost -p 5432 -U cash_flow_user -d cash_flow_db -f migrations/002_increase_token_field_length.sql

# Run nullable fields fix
psql -h localhost -p 5432 -U cash_flow_user -d cash_flow_db -f migrations/003_fix_session_nullable_fields.sql
```

### 6. Start Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Test the API

### 1. Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
    "status": "ok",
    "timestamp": "2025-05-08T09:30:00.000Z"
}
```

### 2. Register User

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123",
    "full_name": "Test User"
  }'
```

### 3. Login User

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Password123"
  }'
```

### 4. Using Postman

1. Import `postman_enhanced_collection.json`
2. Set environment variable `baseUrl` = `http://localhost:5000`
3. Run authentication flow tests

## Common Issues & Solutions

### Database Connection Issues

**Error**: `connection to server at "140.245.50.242", port 5432 failed: Connection timed out`

**Solution**: 
- Ensure SSH tunnel is running: `ssh -N -L 5432:localhost:5432 cash_flow_service@140.245.50.242`
- Use `DB_HOST=localhost` in `.env` file

**Error**: `FATAL: database "cash_flow_db" does not exist`

**Solution**:
- Create database: `createdb cash_flow_db`
- Or run migration script which creates tables

### Token Length Issues

**Error**: `value too long for type character varying(255)`

**Solution**:
- Run migration 002: `psql -h localhost -p 5432 -U cash_flow_user -d cash_flow_db -f migrations/002_increase_token_field_length.sql`

### Null Constraint Issues

**Error**: `null value in column "expires_at" violates not-null constraint`

**Solution**:
- Run migration 003: `psql -h localhost -p 5432 -U cash_flow_user -d cash_flow_db -f migrations/003_fix_session_nullable_fields.sql`

### Validation Errors

**Error**: `Password must contain at least one uppercase letter`

**Solution**:
- Use strong password: minimum 8 chars, 1 uppercase, 1 lowercase, 1 digit
- Example: `Password123`

## Development Workflow

### 1. Make Changes
- Edit source code
- Test with Postman or curl

### 2. Database Changes
- Create new migration file: `004_your_change.sql`
- Create rollback: `rollback/004_rollback_your_change.sql`
- Test migration on development database

### 3. Testing
```bash
# Run all Postman tests
# Import collection and use "Run Collection" feature

# Manual testing
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "dev_user", "email": "dev@example.com", "password": "Password123", "full_name": "Dev User"}'
```

## API Endpoints Overview

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Transactions
- `POST /api/v1/transaction` - Create transaction
- `GET /api/v1/transaction` - Get transactions with pagination

### Assets
- `GET /api/v1/asset` - Get user assets
- `POST /api/v1/asset` - Create new asset

### Reports
- `GET /api/v1/report/monthly` - Monthly financial report
- `GET /api/v1/report/assets` - Asset portfolio summary

### Configuration
- `GET /api/v1/common/categories` - Get transaction categories
- `GET /api/v1/common/wallets` - Get user wallets

## Production Deployment

### Environment Variables
```bash
# Production settings
FLASK_ENV=production
FLASK_DEBUG=False

# Database (use direct connection in production)
DB_HOST=140.245.50.242
DB_PORT=5432
DB_NAME=cash_flow_db
DB_USER=cash_flow_user
DB_PASSWORD=Minhduc24022@1

# Security
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
```

### Using Gunicorn
```bash
# Install Gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Support

For help and support:
1. Check the API documentation: `docs/API_DOCUMENTATION.md`
2. Review the Postman guide: `docs/POSTMAN_COLLECTION_GUIDE.md`
3. Check application logs for detailed error messages
4. Contact the development team

## Next Steps

1. **Explore the API**: Use Postman collection to test all endpoints
2. **Build Client Application**: Use the API documentation to integrate
3. **Add Features**: Extend the API with new endpoints
4. **Deploy**: Set up production environment with proper security

Happy coding! 🚀
