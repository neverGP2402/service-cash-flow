# AI BACKEND RULE

## Architecture
- Use controller -> service -> repository architecture
- Do not write business logic inside controller
- Repository only handles database query
- Service handles business logic

## Naming
- file name: snake_case
- class name: PascalCase
- variable name: snake_case

## API format
- URL: /api/v1/{module}/{endpoint}
- Response must use success_response()

## Request validation
- All POST/PUT APIs must use req class

## Security
- Never trust user_id from frontend
- user_id must get from JWT context

## Database
- Use SQLAlchemy ORM
- Soft delete only
- No raw SQL unless necessary

## Transaction Logic
- Every transaction must:
  - create history
  - update accumulated asset
  - update monthly report

## Logging
- Every exception must log error

## Response
- use read from cash-flow\service-cash-flow\structure-api.txt