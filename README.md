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
## Debugging Purposes
Reset Database
```bash
unset DATABASE_URL
rm -f instance/app.db

python app.py

or

export DATABASE_URL="sqlite:///instance/app.db"
```

Kill backend
```bash
lsof -i :5001 | grep -v COMMAND | awk '{print $2}' | xargs kill -9 2>/dev/null; echo "Killed old process"
```

## Application workflows

- Buyer: browse active auctions and place bids.
- Seller: create items and auctions.
- Admin: view users and auction state.

## Notes

- The backend is built using Flask and Flask-SQLAlchemy.
- The frontend is a lightweight React app with Vite.
- This solution is a working starting point for Phase 3 client application development.

## Known flaws
- the auctionId and bidId are not generated sequentially as integers because it is easier to use React's generateId
