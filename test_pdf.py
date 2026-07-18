import os
from pdf_generator import generate_business_report

store_name = "Mock Store"
ai_data = {
    "insights": ["Sales are up 20%", "Consider stocking more items"],
    "priority_actions": [{"title": "Restock Item A", "description": "Running low", "urgency": "HIGH"}]
}
analytics = {
    "revenue": 50000.50,
    "cost": 30000.00,
    "profit": 20000.50,
    "outstanding_dues": 1500.00,
    "at_risk_customers": [],
    "top_products": [
        {"name": "Product A", "units_sold": 100, "revenue": 10000},
        {"name": "Product B", "units_sold": 50, "revenue": 5000},
    ],
    "dead_stock": []
}
reorder = [
    {"name": "Product C", "current_stock": 5, "reorder_threshold": 10}
]

try:
    buf = generate_business_report(store_name, ai_data, analytics, reorder, "Weekly")
    with open("test_report.pdf", "wb") as f:
        f.write(buf.read())
    print("Successfully generated test_report.pdf")
except Exception as e:
    import traceback
    traceback.print_exc()
