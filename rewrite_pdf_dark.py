import re

with open('pdf_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update charts to use dark theme
dark_charts = """
def _generate_bar_chart(data, labels, title):
    plt.figure(figsize=(6, 3), facecolor='#171617')
    ax = plt.axes()
    ax.set_facecolor('#171617')
    ax.tick_params(colors='#b5b2b2')
    for spine in ax.spines.values():
        spine.set_color('#393939')
    plt.barh(labels[::-1], data[::-1], color='#fe1e34')
    plt.title(title, fontsize=12, fontweight='bold', color='#fcfcfc')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, facecolor='#171617')
    plt.close()
    buf.seek(0)
    return buf

def _generate_donut_chart(revenue, cost):
    plt.figure(figsize=(4, 4), facecolor='#171617')
    ax = plt.axes()
    ax.set_facecolor('#171617')
    profit = max(0, revenue - cost)
    sizes = [cost, profit]
    labels = ['Cost', 'Profit']
    colors = ['#393939', '#10b981']
    if sum(sizes) == 0:
        sizes = [1]
        labels = ['No Data']
        colors = ['#393939']
        
    plt.pie(sizes, labels=labels, colors=colors, startangle=90, wedgeprops=dict(width=0.4, edgecolor='#171617'), textprops={'color': '#b5b2b2'})
    plt.title("Revenue Breakdown", fontsize=12, fontweight='bold', color='#fcfcfc')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, facecolor='#171617')
    plt.close()
    buf.seek(0)
    return buf
"""

# Replace old chart functions
content = re.sub(r'def _generate_bar_chart.*?return buf\n\ndef _generate_donut_chart.*?return buf', dark_charts.strip(), content, flags=re.DOTALL)


# 2. Update generate_business_report to use _base_styles and _table_style instead of light
dark_report = '''
def generate_business_report(store_name, ai_data, analytics, reorder, report_type="Weekly"):
    buffer = io.BytesIO()
    doc = _doc(buffer)
    title_s, sub_s, label_s, body_s, small_s, footer_s, h2_s = _base_styles()
    
    elements = []
    
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    doc_num = f"REP-{now.strftime('%Y%m%d')}"
    
    _header_block(elements, store_name, f"{report_type.upper()} REPORT", doc_num, date_str, title_s, sub_s, small_s)
    
    # 1. Executive Summary
    elements.append(Paragraph("EXECUTIVE SUMMARY", label_s))
    for insight in ai_data.get("insights", []):
        elements.append(Paragraph(f"• {insight}", body_s))
    elements.append(Spacer(1, 10))
    
    # Financial Snapshot with Donut Chart
    elements.append(Paragraph("FINANCIAL SNAPSHOT", label_s))
    
    fin_data = [
        ["Total Revenue", f"₹ {analytics.get('revenue', 0):.2f}"],
        ["Estimated Profit", f"₹ {analytics.get('profit', 0):.2f}"],
        ["Outstanding Dues", f"₹ {analytics.get('outstanding_dues', 0):.2f}"],
        ["High-Risk Customers", str(len(analytics.get('at_risk_customers', [])))]
    ]
    t_fin = Table(fin_data, colWidths=[2*inch, 2*inch])
    t_fin.setStyle(_table_style())
    
    revenue = float(analytics.get('revenue', 0))
    cost = float(analytics.get('cost', 0))
    donut_buf = _generate_donut_chart(revenue, cost)
    donut_img = Image(donut_buf, width=2.5*inch, height=2.5*inch)
    
    # Side-by-side Table and Chart
    fin_layout = Table([[t_fin, donut_img]], colWidths=[4*inch, 3*inch])
    fin_layout.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    elements.append(fin_layout)
    elements.append(Spacer(1, 15))
    
    # Sales Performance with Bar Chart
    elements.append(Paragraph("TOP PERFORMING PRODUCTS", label_s))
    top_products = analytics.get('top_products', [])[:5]
    if top_products:
        labels = [p['name'][:15] + ('...' if len(p['name'])>15 else '') for p in top_products]
        data = [p['revenue'] for p in top_products]
        bar_buf = _generate_bar_chart(data, labels, "Top Products by Revenue (₹)")
        bar_img = Image(bar_buf, width=5*inch, height=2.5*inch)
        elements.append(bar_img)
        
        top_data = [["Product Name", "Units Sold", "Revenue (₹)"]]
        for p in top_products:
            top_data.append([p['name'], str(p['units_sold']), f"{p['revenue']:.2f}"])
        t_top = Table(top_data, colWidths=[3.5*inch, 1.5*inch, 2*inch])
        t_top.setStyle(_table_style())
        elements.append(t_top)
    else:
        elements.append(Paragraph("No sales data available this period.", body_s))
    elements.append(Spacer(1, 15))
    
    # Inventory Alerts
    elements.append(Paragraph("INVENTORY ALERTS", label_s))
    if reorder:
        reorder_data = [["Product Name", "Current Stock", "Threshold"]]
        for p in reorder:
            reorder_data.append([p['name'], str(p['current_stock']), str(p['reorder_threshold'])])
        t_reorder = Table(reorder_data, colWidths=[4*inch, 1.5*inch, 1.5*inch])
        t_reorder.setStyle(_table_style())
        elements.append(t_reorder)
    else:
        elements.append(Paragraph("No immediate restocking needed.", body_s))
    elements.append(Spacer(1, 15))
    
    # Recommended Actions
    elements.append(Paragraph("AI RECOMMENDED ACTIONS", label_s))
    for action in ai_data.get("priority_actions", []):
        urgency = str(action.get("urgency", "")).upper()
        color = "#fe1e34" if urgency == "HIGH" else ("#f39c12" if urgency == "WARNING" else "#10b981")
        elements.append(Paragraph(f"<b><font color='{color}'>[{urgency}]</font> {action.get('title', '')}:</b> {action.get('description', '')}", body_s))
        elements.append(Spacer(1, 5))
        
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated by Vantage Analytics Agent · {date_str}", footer_s))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer
'''

content = re.sub(r'def generate_business_report\(.*?\n# ─── 2\. Purchase Order ────────────────────────────────────────────────────────', dark_report + '\n# ─── 2. Purchase Order ────────────────────────────────────────────────────────', content, flags=re.DOTALL)

# Set page background to dark
page_bg = """
def _doc(buffer, pagesize=letter):
    def bg_color(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#171617"))
        canvas.rect(0, 0, pagesize[0], pagesize[1], fill=1, stroke=0)
        canvas.restoreState()
        
    doc = SimpleDocTemplate(
        buffer, pagesize=pagesize,
        rightMargin=0.65*inch, leftMargin=0.65*inch,
        topMargin=0.7*inch, bottomMargin=0.7*inch
    )
    # We must patch the build method to add the background to every page
    original_build = doc.build
    def build_with_bg(flowables):
        original_build(flowables, onFirstPage=bg_color, onLaterPages=bg_color)
    doc.build = build_with_bg
    return doc
"""
content = re.sub(r'def _doc\(buffer, pagesize=letter\):.*?return SimpleDocTemplate\([^)]*\)', page_bg.strip(), content, flags=re.DOTALL)

with open('pdf_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pdf_generator.py successfully.")
