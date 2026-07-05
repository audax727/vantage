# Vantage — Smart Retail Operations Platform

One transaction pipeline — sale → inventory → ledger → analytics — with four
honest lenses on the same data. Built for kirana stores, small retail shops,
and boutiques.

## What's inside

```
vantage/
├── app.py                  # Full Flask backend (auth, products, sales, ledger, analytics, storefront, AI chat)
├── requirements.txt
├── .env.example             # Copy to .env and fill in what you have
├── templates/                # Multi-section frontend (Jinja2 + vanilla JS)
│   ├── base.html             # Sidebar layout shared by all logged-in pages
│   ├── login.html            # Email + Google sign-in
│   ├── signup.html           # Email + Google sign-up
│   ├── dashboard.html        # Overview: revenue, dues, reorder alerts, at-risk customers
│   ├── products.html         # Inventory CRUD + restock
│   ├── sales.html            # Record a sale (multi-item, auto stock/ledger updates)
│   ├── ledger.html           # Outstanding dues, collect payment, send reminder
│   ├── analytics.html        # Top products, dead stock, profit margin, 7-day forecast
│   └── storefront.html       # Public online storefront + AI chat widget
├── static/
│   ├── style.css              # Design system (ledger/kirana-inspired)
│   └── app.js                 # Shared fetch/toast helpers
└── sample_data/                # Reference CSVs used to seed realistic demo data
    ├── sample_products.csv
    ├── sample_customers.csv
    └── sample_sales.csv
```

## Setup

```bash
cd vantage
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in whatever keys you have (all optional except FLASK_SECRET_KEY)
python app.py
```

Open **http://localhost:5000** — you'll land on the sign-up page. Create an
account (email/password works with zero configuration), then click
**"Load sample data"** on the dashboard to populate products, customers, and
a few historical sales matching `sample_data/`.

### Using with Antigravity
Paste the contents of `app.py`, then create each file under `templates/` and
`static/` with the exact paths shown above — the app expects that folder
structure (Flask looks for `templates/` and `static/` next to `app.py`
automatically). Run with `python app.py`.

## API keys — what you actually need

| Key | Required? | What it powers | Without it |
|---|---|---|---|
| `FLASK_SECRET_KEY` | Recommended | Signs session cookies | A random one is generated each restart, which logs everyone out |
| `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` | Optional | "Continue with Google" | Email/password login still works fully; Google button is hidden |
| `ANTHROPIC_API_KEY` | Optional | AI chat widget on the storefront (product Q&A) | Falls back to simple keyword matching against your catalog — never breaks |
| `EMAIL_ADDRESS` / `EMAIL_APP_PASSWORD` | Optional | Real email for payment reminders / cart nudges / low-stock alerts | Notifications are logged in "mock mode" and still show in the UI |

### Getting each key

- **Google OAuth**: [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials) → Create OAuth Client ID (Web application) → add `http://localhost:5000/auth/google/callback` as an authorized redirect URI.
- **Anthropic API key**: [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) — a few dollars of usage covers an entire demo.
- **Gmail App Password**: enable 2-Step Verification on the Gmail account, then generate a password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). This is a 16-character password, not your normal Gmail password.

Vantage runs completely with **zero keys set** — every integration has a
safe, visible fallback so a live demo never breaks.

## How data flows (the core design)

```
Sale Recorded
   → Stock deducted automatically (stock_movements logged)
   → If underpaid: ledger entry auto-created against the customer
   → If stock crosses reorder_threshold: flagged on the reorder list, ranked by 7-day sales velocity
   → Analytics (profit, top products, dead stock, forecast, at-risk customers) all read from the same tables
```

Everything derives from one schema: `products → sales → sale_items →
ledger_entries → stock_movements`, with `channel` (`in_store` / `online`)
distinguishing storefront orders from counter sales. No second schema was
introduced for the storefront, chat widget, or notifications — see `app.py`
for the full table definitions.

## Security notes

- Passwords are hashed with Werkzeug's `generate_password_hash` (PBKDF2) — never stored in plain text.
- Google-authenticated accounts have no password hash at all (`auth_provider = 'google'`).
- Sessions are signed cookies via Flask's `secret_key` — set `FLASK_SECRET_KEY` in production so sessions survive restarts.
- All API routes (except the public storefront and its chat/order endpoints) require login via `@login_required` and are scoped to `session['user_id']` — one shop can never see another's data.
- For production, put this behind HTTPS and consider migrating from SQLite to Postgres if you expect concurrent writers.

## Not included (by design, for a lean build)

- Real payment processing (Stripe/Razorpay) — the app tracks paid/partial/credit status only, matching how these shops actually operate.
- Barcode/scanner integration — manual product selection is the honest MVP.
- Multi-location is schema-ready (`location_id` on `products`) but the UI currently shows one location; extend `products.html` with a location filter if needed.
