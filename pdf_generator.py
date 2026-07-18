import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import Image

import io
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors
from reportlab.lib.units import inch

# ─── Shared helpers ───────────────────────────────────────────────────────────

BRAND_RED   = colors.HexColor("#fe1e34")
DARK_BG     = colors.HexColor("#171617")
SURFACE     = colors.HexColor("#262525")
TEXT_MAIN   = colors.HexColor("#fcfcfc")
TEXT_MUTED  = colors.HexColor("#b5b2b2")
BORDER      = colors.HexColor("#393939")
ROW_ALT     = colors.HexColor("#1e1d1e")
GREEN       = colors.HexColor("#10b981")


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

def _base_styles():
    styles = getSampleStyleSheet()
    title   = ParagraphStyle('VTitle',   parent=styles['Normal'], fontSize=22, fontName='Helvetica-Bold',   textColor=TEXT_MAIN,  leading=28, spaceAfter=2)
    sub     = ParagraphStyle('VSub',     parent=styles['Normal'], fontSize=10, fontName='Helvetica',        textColor=TEXT_MUTED, leading=14)
    label   = ParagraphStyle('VLabel',   parent=styles['Normal'], fontSize=9,  fontName='Helvetica-Bold',   textColor=BRAND_RED,  leading=12, spaceBefore=14, spaceAfter=2)
    body    = ParagraphStyle('VBody',    parent=styles['Normal'], fontSize=10, fontName='Helvetica',        textColor=TEXT_MAIN,  leading=15)
    small   = ParagraphStyle('VSmall',   parent=styles['Normal'], fontSize=8,  fontName='Helvetica',        textColor=TEXT_MUTED, leading=12)
    footer  = ParagraphStyle('VFooter',  parent=styles['Normal'], fontSize=8,  fontName='Helvetica',        textColor=TEXT_MUTED, alignment=1)
    h2      = ParagraphStyle('VH2',      parent=styles['Normal'], fontSize=13, fontName='Helvetica-Bold',   textColor=TEXT_MAIN,  leading=18, spaceBefore=18, spaceAfter=6)
    return title, sub, label, body, small, footer, h2

def _table_style(header_bg=None):
    hbg = header_bg or SURFACE
    return TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  hbg),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  TEXT_MUTED),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  8),
        ('BOTTOMPADDING', (0, 0), (-1, 0),  10),
        ('TOPPADDING',    (0, 0), (-1, 0),  10),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (-1, -1), TEXT_MAIN),
        ('BACKGROUND',    (0, 1), (-1, -1), DARK_BG),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [DARK_BG, ROW_ALT]),
        ('TOPPADDING',    (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 9),
        ('LEFTPADDING',   (0, 0), (-1, -1), 12),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 12),
        ('LINEBELOW',     (0, 0), (-1, 0),  0.5, BRAND_RED),
        ('LINEBELOW',     (0, 1), (-1, -2), 0.3, BORDER),
        ('ROWSPAN',       (0, 0), (0, 0),   1),
    ])

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

def _header_block(elements, store_name, doc_type, doc_number, date_str, title_s, sub_s, small_s):
    """Renders the standard two-column header: left=store, right=doc details."""
    header_data = [[
        Paragraph(f"<b>{store_name}</b>", title_s),
        Paragraph(f"<b>{doc_type}</b><br/><font size=9 color='#b5b2b2'>{doc_number}</font>", title_s)
    ], [
        Paragraph("Issued via <b>Vantage</b>", small_s),
        Paragraph(f"Date: {date_str}", small_s)
    ]]
    ht = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
    ht.setStyle(TableStyle([
        ('ALIGN',        (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR',    (1, 0), (1, 0), BRAND_RED),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 4),
        ('TOPPADDING',   (0, 0), (-1, -1), 0),
    ]))
    elements.append(ht)
    elements.append(HRFlowable(width="100%", thickness=0.5, color=BRAND_RED, spaceAfter=16))


# ─── 1. Business Report (existing) ───────────────────────────────────────────



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
    elements.append(Paragraph("RECOMMENDED ACTIONS", label_s))
    for action in ai_data.get("priority_actions", []):
        urgency = str(action.get("urgency", "")).upper()
        color = "#fe1e34" if urgency == "HIGH" else ("#f39c12" if urgency == "WARNING" else "#10b981")
        elements.append(Paragraph(f"<b><font color='{color}'>[{urgency}]</font> {action.get('title', '')}:</b> {action.get('description', '')}", body_s))
        elements.append(Spacer(1, 5))
        
    elements.append(Spacer(1, 30))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated by Vantage Analytics · {date_str}", footer_s))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer

# ─── 2. Purchase Order ────────────────────────────────────────────────────────

def generate_purchase_order(store_name, supplier_name, supplier_contact, items, po_number=None):
    """
    items: list of dicts with keys: name, unit, qty, cost_price
    """
    buffer = io.BytesIO()
    doc = _doc(buffer)
    title_s, sub_s, label_s, body_s, small_s, footer_s, h2_s = _base_styles()
    elements = []

    now = datetime.now()
    po_num = po_number or f"PO-{now.strftime('%Y%m%d-%H%M')}"
    date_str = now.strftime("%d %B %Y")

    _header_block(elements, store_name, "PURCHASE ORDER", po_num, date_str, title_s, sub_s, small_s)

    # Supplier info box
    elements.append(Paragraph("SUPPLIER", label_s))
    supplier_data = [
        [Paragraph(f"<b>{supplier_name}</b>", body_s), ""],
        [Paragraph(f"{supplier_contact}", small_s), ""],
    ]
    st = Table(supplier_data, colWidths=[3*inch, 4*inch])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), SURFACE),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(st)
    elements.append(Spacer(1, 18))

    # Items table
    elements.append(Paragraph("ORDER DETAILS", label_s))
    elements.append(Spacer(1, 6))

    table_data = [["#", "Product / Description", "Unit", "Qty", "Unit Cost (₹)", "Line Total (₹)"]]
    grand_total = 0.0
    for i, item in enumerate(items, 1):
        qty = float(item.get("qty", 0))
        cost = float(item.get("cost_price", 0))
        line = qty * cost
        grand_total += line
        table_data.append([
            str(i),
            item.get("name", ""),
            item.get("unit", "pcs"),
            f"{qty:g}",
            f"{cost:.2f}",
            f"{line:.2f}",
        ])

    col_w = [0.35*inch, 2.5*inch, 0.6*inch, 0.5*inch, 1.1*inch, 1.2*inch]
    t = Table(table_data, colWidths=col_w)
    ts = _table_style()
    ts.add('ALIGN', (0, 0), (0, -1), 'CENTER')
    ts.add('ALIGN', (3, 0), (5, -1), 'RIGHT')
    t.setStyle(ts)
    elements.append(t)

    # Grand total row
    elements.append(Spacer(1, 6))
    total_data = [["", "", "", "", "GRAND TOTAL", f"₹ {grand_total:.2f}"]]
    tt = Table(total_data, colWidths=col_w)
    tt.setStyle(TableStyle([
        ('FONTNAME',      (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 11),
        ('TEXTCOLOR',     (4, 0), (4, 0),   TEXT_MUTED),
        ('TEXTCOLOR',     (5, 0), (5, 0),   BRAND_RED),
        ('ALIGN',         (4, 0), (5, 0),   'RIGHT'),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('LINEABOVE',     (4, 0), (5, 0),   0.5, BORDER),
    ]))
    elements.append(tt)

    # Notes
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("NOTES", label_s))
    elements.append(Paragraph("Please confirm receipt of this order and expected delivery date. All prices in INR.", body_s))

    # Footer
    elements.append(Spacer(1, 36))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated by Vantage · {date_str} · This is a system-generated purchase order.", footer_s))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ─── 3. Customer Statement ────────────────────────────────────────────────────

def generate_customer_statement(store_name, customer_name, customer_phone, customer_email,
                                 open_balance, entries):
    """
    entries: list of dicts with keys: date, sale_id, total_amount, amount_paid, balance, notes
    """
    buffer = io.BytesIO()
    doc = _doc(buffer)
    title_s, sub_s, label_s, body_s, small_s, footer_s, h2_s = _base_styles()
    elements = []

    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    stmt_num = f"STMT-{now.strftime('%Y%m%d-%H%M')}"

    _header_block(elements, store_name, "ACCOUNT STATEMENT", stmt_num, date_str, title_s, sub_s, small_s)

    # Customer info + summary box side by side
    contact_lines = customer_name
    if customer_phone:
        contact_lines += f"<br/>{customer_phone}"
    if customer_email:
        contact_lines += f"<br/>{customer_email}"

    balance_color = "#fe1e34" if open_balance > 0 else "#10b981"
    balance_label = "AMOUNT OUTSTANDING" if open_balance > 0 else "BALANCE"

    info_data = [[
        Paragraph(f"<b>BILLED TO</b><br/><b>{customer_name}</b><br/>"
                  f"<font size=9 color='#b5b2b2'>{customer_phone or ''}</font><br/>"
                  f"<font size=9 color='#b5b2b2'>{customer_email or ''}</font>", body_s),
        Paragraph(
            f"<font size=9 color='#b5b2b2'>{balance_label}</font><br/>"
            f"<font size=22 color='{balance_color}'><b>₹ {open_balance:.2f}</b></font><br/>"
            f"<font size=8 color='#b5b2b2'>As of {date_str}</font>",
            ParagraphStyle('bal', parent=body_s, alignment=2)
        )
    ]]
    info_t = Table(info_data, colWidths=[3.5*inch, 3.5*inch])
    info_t.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), SURFACE),
        ('BOX',          (0, 0), (-1, -1), 0.5, BORDER),
        ('LEFTPADDING',  (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING',   (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 14),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(info_t)
    elements.append(Spacer(1, 20))

    # Transaction history
    elements.append(Paragraph("TRANSACTION HISTORY", label_s))
    elements.append(Spacer(1, 6))

    if entries:
        table_data = [["Date", "Sale #", "Invoice Total (₹)", "Amount Paid (₹)", "Balance (₹)"]]
        running = 0.0
        for e in entries:
            try:
                d = datetime.fromisoformat(str(e.get("date", ""))).strftime("%d %b %Y")
            except Exception:
                d = str(e.get("date", ""))
            due = float(e.get("amount_due", 0))
            paid = float(e.get("amount_paid", 0))
            bal = due - paid
            running += bal
            table_data.append([
                d,
                f"#{e.get('sale_id', '—')}",
                f"{due:.2f}",
                f"{paid:.2f}",
                f"{bal:.2f}",
            ])

        col_w = [1.2*inch, 0.9*inch, 1.5*inch, 1.5*inch, 1.2*inch]
        t = Table(table_data, colWidths=col_w)
        ts = _table_style()
        ts.add('ALIGN', (2, 0), (4, -1), 'RIGHT')
        t.setStyle(ts)
        elements.append(t)
    else:
        elements.append(Paragraph("No transaction records found.", body_s))

    # Summary footer
    elements.append(Spacer(1, 10))
    summary_data = [["", "", "", "TOTAL OUTSTANDING", f"₹ {open_balance:.2f}"]]
    col_w = [1.2*inch, 0.9*inch, 1.5*inch, 1.5*inch, 1.2*inch]
    st = Table(summary_data, colWidths=col_w)
    st.setStyle(TableStyle([
        ('FONTNAME',  (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',  (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (3, 0), (3, 0),   TEXT_MUTED),
        ('TEXTCOLOR', (4, 0), (4, 0),   BRAND_RED),
        ('ALIGN',     (3, 0), (4, 0),   'RIGHT'),
        ('TOPPADDING',(0, 0), (-1, -1), 8),
        ('LINEABOVE', (3, 0), (4, 0),   0.5, BORDER),
    ]))
    elements.append(st)

    elements.append(Spacer(1, 36))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"Generated by Vantage · {date_str} · Please contact us if you have questions about this statement.",
        footer_s
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# ─── 4. Quotation ─────────────────────────────────────────────────────────────

def generate_quotation(store_name, quote_id, customer_name, customer_phone, customer_email,
                        items, subtotal, discount_pct, total_amount, cgst_amount=0, sgst_amount=0, gstin="", notes=""):
    """
    items: list of dicts with keys: name, qty, unit, unit_price, line_total, gst_rate
    """
    buffer = io.BytesIO()
    doc = _doc(buffer)
    title_s, sub_s, label_s, body_s, small_s, footer_s, h2_s = _base_styles()
    elements = []

    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    from datetime import timedelta
    valid_until = (now + timedelta(days=15)).strftime("%d %B %Y")
    quote_num = f"Q-{str(quote_id).zfill(5)}"

    # If GSTIN exists, append it to store name
    if gstin:
        store_name_display = f"{store_name}<br/><font size=9 color='#b5b2b2'>GSTIN: {gstin}</font>"
    else:
        store_name_display = store_name

    _header_block(elements, store_name_display, "PROFORMA INVOICE", quote_num, date_str, title_s, sub_s, small_s)

    # Customer + validity
    validity_label = ParagraphStyle('vl', parent=small_s, alignment=2)
    cust_data = [[
        Paragraph(
            f"<b>PREPARED FOR</b><br/><b>{customer_name}</b><br/>"
            f"<font size=9 color='#b5b2b2'>{customer_phone or ''}</font><br/>"
            f"<font size=9 color='#b5b2b2'>{customer_email or ''}</font>",
            body_s
        ),
        Paragraph(
            f"<font size=9 color='#b5b2b2'>Valid Until</font><br/>"
            f"<b><font size=13>{valid_until}</font></b><br/>"
            f"<font size=8 color='#b5b2b2'>15 days from issue date</font>",
            validity_label
        )
    ]]
    ct = Table(cust_data, colWidths=[3.5*inch, 3.5*inch])
    ct.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), SURFACE),
        ('BOX',          (0, 0), (-1, -1), 0.5, BORDER),
        ('LEFTPADDING',  (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING',   (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 14),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(ct)
    elements.append(Spacer(1, 20))

    # Line items
    elements.append(Paragraph("ITEMS & PRICING", label_s))
    elements.append(Spacer(1, 6))

    table_data = [["#", "Description", "Unit", "Qty", "Unit Price (₹)", "Amount (₹)"]]
    for i, item in enumerate(items, 1):
        gst_str = f"<br/><font size=7 color='#b5b2b2'>GST: {item.get('gst_rate', 18)}%</font>" if float(item.get("gst_rate", 0)) > 0 else ""
        desc_cell = Paragraph(f"{item.get('name', '')}{gst_str}", small_s)
        
        table_data.append([
            str(i),
            desc_cell,
            item.get("unit", "pcs"),
            f"{float(item.get('qty', 0)):g}",
            f"{float(item.get('unit_price', 0)):.2f}",
            f"{float(item.get('line_total', 0)):.2f}",
        ])

    col_w = [0.35*inch, 2.5*inch, 0.6*inch, 0.5*inch, 1.1*inch, 1.2*inch]
    t = Table(table_data, colWidths=col_w)
    ts = _table_style()
    ts.add('ALIGN', (0, 0), (0, -1), 'CENTER')
    ts.add('ALIGN', (3, 0), (5, -1), 'RIGHT')
    ts.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    t.setStyle(ts)
    elements.append(t)

    # Subtotal / Discount / Taxes / Total
    elements.append(Spacer(1, 6))
    
    totals = [
        ["", "", "", "", "Gross Total", f"₹ {subtotal:.2f}"],
    ]
    if discount_pct > 0:
        disc_amt = subtotal * discount_pct / 100
        totals.append(["", "", "", "", f"Discount ({discount_pct:.1f}%)", f"- ₹ {disc_amt:.2f}"])
        
    net_total = subtotal - (subtotal * discount_pct / 100) if discount_pct > 0 else subtotal
    total_tax = cgst_amount + sgst_amount
    taxable_val = net_total - total_tax

    totals.append(["", "", "", "", "Taxable Value", f"₹ {taxable_val:.2f}"])
    
    if cgst_amount > 0 or sgst_amount > 0:
        totals.append(["", "", "", "", "CGST", f"+ ₹ {float(cgst_amount):.2f}"])
        totals.append(["", "", "", "", "SGST", f"+ ₹ {float(sgst_amount):.2f}"])
        
    totals.append(["", "", "", "", "GRAND TOTAL", f"₹ {float(total_amount):.2f}"])

    tt = Table(totals, colWidths=col_w)
    total_rows = len(totals)
    tt.setStyle(TableStyle([
        ('FONTNAME',      (4, 0), (5, -1),  'Helvetica'),
        ('FONTNAME',      (4, total_rows-1),(5, total_rows-1), 'Helvetica-Bold'),
        ('FONTSIZE',      (4, total_rows-1),(5, total_rows-1), 11),
        ('TEXTCOLOR',     (4, 0), (4, -1),  TEXT_MUTED),
        ('TEXTCOLOR',     (5, 0), (5, -2),  TEXT_MAIN),
        ('TEXTCOLOR',     (5, total_rows-1),(5, total_rows-1), BRAND_RED),
        ('ALIGN',         (4, 0), (5, -1),  'RIGHT'),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LINEABOVE',     (4, total_rows-1),(5, total_rows-1), 0.5, BORDER),
    ]))
    elements.append(tt)

    # Notes + Terms
    if notes:
        elements.append(Spacer(1, 16))
        elements.append(Paragraph("NOTES", label_s))
        elements.append(Paragraph(notes, body_s))

    elements.append(Spacer(1, 16))
    elements.append(Paragraph("TERMS & CONDITIONS", label_s))
    terms = [
        "• This quotation is valid for 15 days from the date of issue.",
        "• Prices are subject to change if not accepted within the validity period.",
        "• Goods remain the property of the seller until full payment is received.",
        "• Please reference the quotation number on your purchase order.",
    ]
    for term in terms:
        elements.append(Paragraph(term, small_s))

    elements.append(Spacer(1, 36))
    elements.append(HRFlowable(width="100%", thickness=0.3, color=BORDER))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"Generated by Vantage · {date_str} · {quote_num} · Thank you for your business.",
        footer_s
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
