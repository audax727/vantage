<div align="center">
  <br>
  <h1>Vantage</h1>
  <p><strong>Retail Intelligence & POS ERP for SMEs</strong></p>
  <p><em>The speed you need. The clarity you deserve.</em></p>
  <br>
</div>

---

## 🚀 Overview

**Vantage** is a lightning-fast, beautifully designed, all-in-one ERP built specifically for retail SMEs and wholesale distributors. 

Today, local retail operates in a state of digital fragmentation. Businesses use one clunky, outdated system to ring up sales, a separate Excel sheet to track inventory, and often physical paper notebooks to manage customer credit and dues. 

Vantage unifies **Point-of-Sale checkout, real-time inventory tracking, and digital ledger management** into a single cloud platform. It’s designed to be proactive, telling owners exactly what needs attention rather than just acting as a static database.

## ✨ Key Features

*   **⚡ Lightning POS:** Sub-second checkout speed. As you type a customer's name, the system finds them instantly. Auto-calculates subtotals, GST, and custom discounts.
*   **📖 Unified Digital Ledger:** Built directly into the checkout flow. If a customer needs credit, mark the sale as **'Due'**. Inventory drops, the sale records, and the debt pushes to the Ledger instantly. Zero double data entry.
*   **📦 Smart Inventory & ERP:** A searchable, scalable catalog. Monitor pricing, margins, categories, and live stock levels. Features bulk CSV import/export.
*   **📈 Proactive Dashboard:** Get a live pulse of your operation: Revenue, Profit, and Outstanding Dues. Vantage proactively alerts you to low-stock items (ranked by velocity) and highlights at-risk customers.
*   **📄 B2B Quotations:** Instantly draft professional estimates and convert them to live sales with one click.
*   **🎨 Premium UI/UX:** Built on the striking **"SVZ Black Gallery"** design system. Features high-contrast Dark Mode, custom cursors, fluid view transitions, and an interactive AI terminal aesthetic.

## 🛠 Tech Stack

*   **Backend:** Python, Flask
*   **Database:** PostgreSQL (Production) / SQLite (Local MVP)
*   **Frontend:** HTML5, CSS3 (Vanilla), JavaScript
*   **Design System:** SVZ Black Gallery (Void Black, Charcoal, Heartbeat Red)
*   **Typography:** Inter (Display), Playfair Display (Accents), Fira Code (Mono)

## 💻 Setup Instructions (Local Development)

To run Vantage locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/vantage.git
   cd vantage
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   ```bash
   cp .env.example .env
   ```
   *Note: Vantage is designed to run locally even without API keys (they will gracefully fall back to mock modes).*

5. **Run the application:**
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`. You can create an account and click **"Load sample data"** on the dashboard to populate the app with realistic products and sales.

## 🛡 Security & Architecture

- **Data Flow:** One transaction pipeline — `sale → inventory → ledger → analytics`.
- **Authentication:** Werkzeug PBKDF2 password hashing & Google OAuth integration.
- **Isolation:** All routes are scoped to `session['user_id']`. One shop can never see another's data.

---
<div align="center">
  <p>Built to Scale. Built for Speed.</p>
</div>
