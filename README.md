# CS166-Final-Project

This repository now includes a simple auction client application built with React and Flask, backed by PostgreSQL-compatible database access.

## Project structure

- `schema.sql` — PostgreSQL schema for Users, Items, Auctions, Payments, Shipments, and Bids.
- `backend/` — Flask backend service with SQLAlchemy database models and REST API endpoints.
- `frontend/` — React + Vite client application for Buyer, Seller, and Admin workflows.

## Running the backend

1. Open a terminal in `backend/`.
2. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure the database URL if you want to use PostgreSQL. For PostgreSQL, set:
   ```bash
   export DATABASE_URL=postgresql://user:password@localhost:5432/auction_db
   ```
   If `DATABASE_URL` is not set or cannot be reached, the backend now falls back to `sqlite:///app.db` for local testing.
4. Start the backend:
   ```bash
   python app.py
   ```

## Running the frontend

1. Open a terminal in `frontend/`.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React app:
   ```bash
   npm run dev
   ```
4. Open the browser at `http://localhost:5173`.

## Seed sample data

Use the backend seed endpoint to create sample users, an item, and an auction:

```bash
curl -X POST http://localhost:5001/api/seed
```

## Database Setup

1. Install PostgreSQL 15:


brew install postgresql@15

brew services start postgresql@15

2. Create the database and load everything:
createdb auction_db
psql -d auction_db -f schema.sql
psql -d auction_db -f data.sql
psql -d auction_db -f indexes.sql

## Sample Data

The dataset is themed around classic cars and automotive parts. It includes:
- 10 users (1 Admin, 4 Sellers, 5 Buyers)
- 12 items (6 classic cars, 4 car parts, 2 collectibles)
- 12 auctions (8 Active, 4 Closed)
- 21 bids, 4 payments, 4 shipments

Test credentials:
| Login | Password | Role |
|-------|----------|------|
| admin1 | admin123 | Admin |
| seller1 | pass1234 | Seller |
| buyer1 | pass1234 | Buyer |

## Physical Database Design

Performance indexes are defined in `indexes.sql`. They target the most frequently queried columns:
- `auction(auction_status)` — buyers always filter by Active/Closed
- `bid(auction_id)` — every auction view joins on this
- `item(category)` — buyers browse by category
- `bid(buyer_login)` — buyers check their own bid history
- `payment(auction_id)` — post-auction payment lookups
- `shipment(auction_id)` — shipment tracking lookups
- `auction(seller_login)` — seller dashboard queries
- `bid(bid_timestamp)` — chronological bid sorting


## Application workflows

- Buyer: browse active auctions and place bids.
- Seller: create items and auctions.
- Admin: view users and auction state.

## Notes

- The backend is built using Flask and Flask-SQLAlchemy.
- The frontend is a lightweight React app with Vite.
- This solution is a working starting point for Phase 3 client application development.
