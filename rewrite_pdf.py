import re

with open('pdf_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add matplotlib and Image imports at the top
imports_to_add = """import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import Image
"""
if "import matplotlib" not in content:
    content = content.replace("import io", imports_to_add + "\nimport io")

# 2. Add Light Theme Variables and Styles below existing theme variables
light_theme_vars = """
# LIGHT THEME
L_BG        = colors.HexColor("#ffffff")
L_SURFACE   = colors.HexColor("#f8f9fa")
L_TEXT_MAIN = colors.HexColor("#212529")
L_TEXT_MUTED= colors.HexColor("#6c757d")
L_BORDER    = colors.HexColor("#dee2e6")
L_ROW_ALT   = colors.HexColor("#fdfdfd")

def _light_styles():
    styles = getSampleStyleSheet()
    title   = ParagraphStyle('VTitle',   parent=styles['Normal'], fontSize=22, fontName='Helvetica-Bold',   textColor=L_TEXT_MAIN,  leading=28, spaceAfter=2)
    sub     = ParagraphStyle('VSub',     parent=styles['Normal'], fontSize=10, fontName='Helvetica',        textColor=L_TEXT_MUTED, leading=14)
    label   = ParagraphStyle('VLabel',   parent=styles['Normal'], fontSize=9,  fontName='Helvetica-Bold',   textColor=BRAND_RED,  leading=12, spaceBefore=14, spaceAfter=2)
    body    = ParagraphStyle('VBody',    parent=styles['Normal'], fontSize=10, fontName='Helvetica',        textColor=L_TEXT_MAIN,  leading=15)
    small   = ParagraphStyle('VSmall',   parent=styles['Normal'], fontSize=8,  fontName='Helvetica',        textColor=L_TEXT_MUTED, leading=12)
    footer  = ParagraphStyle('VFooter',  parent=styles['Normal'], fontSize=8,  fontName='Helvetica',        textColor=L_TEXT_MUTED, alignment=1)
    h2      = ParagraphStyle('VH2',      parent=styles['Normal'], fontSize=13, fontName='Helvetica-Bold',   textColor=L_TEXT_MAIN,  leading=18, spaceBefore=18, spaceAfter=6)
    return title, sub, label, body, small, footer, h2

def _light_table_style(header_bg=None):
    hbg = header_bg or L_SURFACE
    return TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  hbg),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  L_TEXT_MUTED),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  8),
        ('BOTTOMPADDING', (0, 0), (-1, 0),  10),
        ('TOPPADDING',    (0, 0), (-1, 0),  10),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (-1, -1), L_TEXT_MAIN),
        ('BACKGROUND',    (0, 1), (-1, -1), L_BG),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [L_BG, L_ROW_ALT]),
        ('TOPPADDING',    (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('LINEBELOW',     (0, 0), (-1, 0),  0.5, BRAND_RED),
        ('LINEBELOW',     (0, 1), (-1, -2), 0.3, L_BORDER),
        ('ROWSPAN',       (0, 0), (0, 0),   1),
    ])

def _generate_bar_chart(data, labels, title):
    plt.figure(figsize=(6, 3))
    plt.barh(labels[::-1], data[::-1], color='#fe1e34')
    plt.title(title, fontsize=12, fontweight='bold', color='#212529')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close()
    buf.seek(0)
    return buf

def _generate_donut_chart(revenue, cost):
    plt.figure(figsize=(4, 4))
    profit = max(0, revenue - cost)
    sizes = [cost, profit]
    labels = ['Cost', 'Profit']
    colors = ['#dee2e6', '#10b981']
    if sum(sizes) == 0:
        sizes = [1]
        labels = ['No Data']
        colors = ['#dee2e6']
        
    plt.pie(sizes, labels=labels, colors=colors, startangle=90, wedgeprops=dict(width=0.4))
    plt.title("Revenue Breakdown", fontsize=12, fontweight='bold', color='#212529')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close()
    buf.seek(0)
    return buf
"""
if "# LIGHT THEME" not in content:
    content = content.replace("def _base_styles():", light_theme_vars + "\ndef _base_styles():")


# 3. Replace the entire generate_business_report function
new_report_code = '''
def generate_business_report(store_name, ai_data, analytics, reorder, report_type="Weekly"):
    buffer = io.BytesIO()
    doc = _doc(buffer)
    title_s, sub_s, label_s, body_s, small_s, footer_s, h2_s = _light_styles()
    
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
    t_fin.setStyle(_light_table_style())
    
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
        t_top.setStyle(_light_table_style())
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
        t_reorder.setStyle(_light_table_style())
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
    elements.append(HRFlowable(width="100%", thickness=0.3, color=L_BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated by Vantage Analytics Agent · {date_str}", footer_s))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer
'''

# Use regex to replace the existing generate_business_report
pattern = re.compile(r"def generate_business_report\(.*?\n# ─── 2\. Purchase Order ────────────────────────────────────────────────────────", re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_report_code + "\n# ─── 2. Purchase Order ────────────────────────────────────────────────────────", content)
else:
    print("Could not find generate_business_report to replace")

with open('pdf_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated pdf_generator.py successfully.")
