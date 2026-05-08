# Cash Flow Management System

Backend service for personal finance management built with Flask.

## Architecture

- Controller -> Service -> Repository
- SQLAlchemy ORM with PostgreSQL
- Soft delete only
- JWT authentication

## Project Structure

See `structure-project.txt` for full layout.

## Modules

- `auth`: Authentication & authorization
- `transaction`: Income/expense transactions
- `debt`: Loan & debt tracking
- `asset`: Asset accumulation & investment tracking
- `report`: Financial reports & analytics
- `common_master`: Wallets, categories, units, exchange rates, assets, counterparties
- `external`: File service, exchange rate clients

## Running

```bash
pip install -r requirements.txt
flask run
```

## Migration

```bash
flask db init
flask db migrate
flask db upgrade
```
