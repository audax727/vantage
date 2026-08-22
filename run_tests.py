import requests
import json
import time

BASE = "http://127.0.0.1:5000"
s = requests.Session()

def run():
    print("--- VANTAGE API TEST SUITE ---")
    
    # 1. Login
    res = s.post(f"{BASE}/login", data={"email": "shrikarreddy19@gmail.com", "password": "nikenduk"})
    assert res.status_code == 200, f"Login failed: {res.text}"
    print("[OK] Login successful")

    # 2. Seed data (to have a clean slate)
    res = s.post(f"{BASE}/api/seed-demo-data")
    assert res.status_code == 200, f"Seed failed: {res.text}"
    print("[OK] Seed successful")

    # 3. Add Product
    res = s.post(f"{BASE}/api/products", json={
        "name": "Test Product",
        "category": "Electronics",
        "cost_price": "100",
        "sell_price": "200",
        "current_stock": "50",
        "reorder_threshold": "5",
        "unit": "pcs",
        "gst_rate": "18.0"
    })
    assert res.status_code == 200, f"Add product failed: {res.text}"
    print("[OK] Add Product successful")

    # Get Products
    res = s.get(f"{BASE}/api/products")
    products = res.json()
    test_product = next(p for p in products if p["name"] == "Test Product")
    pid = test_product["id"]

    # 4. Create Customer
    res = s.post(f"{BASE}/api/customers", json={
        "name": "Test Customer",
        "phone": "1234567890",
        "email": "test@example.com"
    })
    assert res.status_code == 200, f"Add customer failed: {res.text}"
    print("[OK] Add Customer successful")

    res = s.get(f"{BASE}/api/customers")
    customers = res.json()
    test_customer = next(c for c in customers if c["name"] == "Test Customer")
    cid = test_customer["id"]

    # 5. Record Sale (Full payment)
    res = s.post(f"{BASE}/api/sales", json={
        "customer_id": cid,
        "items": [{"product_id": pid, "qty": 2}],
        "amount_paid": 400.0,
        "channel": "in_store"
    })
    assert res.status_code == 200, f"Sale failed: {res.text}"
    print("[OK] Sale (Full) successful")

    # Check stock deduction
    res = s.get(f"{BASE}/api/products")
    products = res.json()
    test_product_new = next(p for p in products if p["id"] == pid)
    assert test_product_new["current_stock"] == 48, f"Stock not deducted: {test_product_new['current_stock']}"
    print("[OK] Stock Deduction successful")

    # 6. Record Sale (Partial payment)
    res = s.post(f"{BASE}/api/sales", json={
        "customer_id": cid,
        "items": [{"product_id": pid, "qty": 1}],
        "amount_paid": 100.0,
        "channel": "in_store"
    })
    assert res.status_code == 200, f"Partial Sale failed: {res.text}"
    print("[OK] Sale (Partial) successful")

    # Check Ledger
    res = s.get(f"{BASE}/api/ledger")
    ledger = res.json()
    test_ledger = [l for l in ledger if l["customer_id"] == cid]
    assert len(test_ledger) > 0, "No ledger entry found"
    entry = test_ledger[0]
    assert entry["amount_due"] == 100.0, f"Incorrect amount due: {entry['amount_due']}"
    print("[OK] Ledger partial entry successful")

    # 7. Settle Payment
    res = s.post(f"{BASE}/api/ledger/{entry['id']}/collect", json={"amount": 100.0})
    assert res.status_code == 200, f"Settle failed: {res.text}"
    print("[OK] Settle Payment successful")

    # Check Ledger again
    res = s.get(f"{BASE}/api/ledger")
    ledger = res.json()
    test_ledger = [l for l in ledger if l["customer_id"] == cid]
    assert len(test_ledger) == 0, "Ledger entry not cleared"
    print("[OK] Ledger settled status successful")

    # 8. Send Reminder
    # Add a mock partial sale first so we have an open entry
    res = s.post(f"{BASE}/api/sales", json={
        "customer_id": cid,
        "items": [{"product_id": pid, "qty": 1}],
        "amount_paid": 50.0,
        "channel": "in_store"
    })
    res = s.get(f"{BASE}/api/ledger")
    entry = [l for l in res.json() if l["customer_id"] == cid][0]
    
    res = s.post(f"{BASE}/api/ledger/remind/{entry['id']}")
    assert res.status_code == 200, f"Send reminder failed: {res.text}"
    print("[OK] Email Reminder successful")

    # 9. Quotations
    res = s.post(f"{BASE}/api/quotations", json={
        "customer_name": "New Prospect",
        "customer_id": None,
        "items": [{"product_id": pid, "name": "Test Product", "qty": "1", "unit": "pcs", "unit_price": "200.00", "line_total": "200.00"}],
        "subtotal": "200.00",
        "discount_pct": "0.00",
        "total_amount": "200.00",
        "notes": ""
    })
    assert res.status_code == 200, f"Create quote failed: {res.text}"
    print("[OK] Create Quotation successful")

    res = s.get(f"{BASE}/api/quotations")
    quotes = res.json()
    q_id = quotes[0]["id"]
    
    res = s.post(f"{BASE}/api/quotations/{q_id}/status", json={"status": "accepted"})
    assert res.status_code == 200, f"Update quote status failed: {res.text}"
    print("[OK] Update Quotation Status successful")

    # 10. AI Chat
    res = s.post(f"{BASE}/api/analytics/ai_chat", json={"question": "What is my total revenue?"})
    assert res.status_code == 200, f"AI chat failed: {res.text}"
    print("[OK] AI Chat successful")

    print("\nALL TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run()
