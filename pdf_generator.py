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
    return SimpleDocTemplate(
        buffer, pagesize=pagesize,
        rightMargin=0.65*inch, leftMargin=0.65*inch,
        topMargin=0.7*inch, bottomMargin=0.7*inch
    )

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
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.textColor = colors.HexColor("#2c3e50")
    
    h2_style = styles['Heading2']
    h2_style.textColor = colors.HexColor("#34495e")
    
    normal = styles['Normal']
    normal.fontSize = 11
    normal.leading = 14
    
    elements = []
    
    elements.append(Paragraph(f"<b>{store_name}</b> - {report_type} Business Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal))
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("1. Executive Summary", h2_style))
    for insight in ai_data.get("insights", []):
        elements.append(Paragraph(f"• {insight}", normal))
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("2. Sales Performance", h2_style))
    elements.append(Paragraph("<b>Top Performers:</b>", normal))
    elements.append(Spacer(1, 5))
    
    top_data = [["Product Name", "Revenue"]]
    for p in analytics.get('top_products', [])[:5]:
        top_data.append([p['name'], f"Rs.{p['revenue']:.2f}"])
        
    if len(top_data) > 1:
        t_top = Table(top_data, colWidths=[300, 100])
        t_top.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f8f9fa")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e9ecef")),
        ]))
        elements.append(t_top)
    else:
        elements.append(Paragraph("No sales data available this period.", normal))
        
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Dead Stock (No sales in 30+ days):</b>", normal))
    elements.append(Spacer(1, 5))
    
    dead_data = [["Product Name", "Current Stock"]]
    for p in analytics.get('dead_stock', [])[:5]:
        dead_data.append([p['name'], str(p['current_stock'])])
        
    if len(dead_data) > 1:
        t_dead = Table(dead_data, colWidths=[300, 100])
        t_dead.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#fff3f3")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#c0392b")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e9ecef")),
        ]))
        elements.append(t_dead)
    else:
        elements.append(Paragraph("No dead stock items detected.", normal))
        
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("3. Inventory Alerts", h2_style))
    if reorder:
        reorder_data = [["Product Name", "Current Stock"]]
        for p in reorder:
            reorder_data.append([p['name'], str(p['current_stock'])])
        t_reorder = Table(reorder_data, colWidths=[300, 100])
        t_reorder.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#fff8e1")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#f39c12")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e9ecef")),
        ]))
        elements.append(t_reorder)
    else:
        elements.append(Paragraph("No immediate restocking needed.", normal))
        
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("4. Financial Snapshot", h2_style))
    fin_data = [
        ["Total Revenue", f"Rs.{analytics.get('revenue', 0):.2f}"],
        ["Estimated Profit", f"Rs.{analytics.get('profit', 0):.2f}"],
        ["Outstanding Dues", f"Rs.{analytics.get('outstanding_dues', 0):.2f}"],
        ["High-Risk Customers", str(len(analytics.get('at_risk_customers', [])))]
    ]
    t_fin = Table(fin_data, colWidths=[200, 200])
    t_fin.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e9ecef")),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f9fa")),
    ]))
    elements.append(t_fin)
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("5. Recommended Actions", h2_style))
    for action in ai_data.get("priority_actions", []):
        urgency = str(action.get("urgency", "")).upper()
        color = "red" if urgency == "HIGH" else ("orange" if urgency == "WARNING" else "green")
        elements.append(Paragraph(f"<b><font color='{color}'>[{urgency}]</font> {action.get('title', '')}:</b> {action.get('description', '')}", normal))
        elements.append(Spacer(1, 5))
        
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'], alignment=1, fontSize=9, textColor=colors.gray
    )
    elements.append(Paragraph("Generated by Vantage Analytics Agent", footer_style))
        
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
                        items, subtotal, discount_pct, total_amount, notes=""):
    """
    items: list of dicts with keys: name, qty, unit, unit_price, line_total
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

    _header_block(elements, store_name, "QUOTATION", quote_num, date_str, title_s, sub_s, small_s)

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
        table_data.append([
            str(i),
            item.get("name", ""),
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
    t.setStyle(ts)
    elements.append(t)

    # Subtotal / Discount / Total
    elements.append(Spacer(1, 6))
    totals = [
        ["", "", "", "", "Subtotal", f"₹ {subtotal:.2f}"],
    ]
    if discount_pct > 0:
        disc_amt = subtotal * discount_pct / 100
        totals.append(["", "", "", "", f"Discount ({discount_pct:.1f}%)", f"- ₹ {disc_amt:.2f}"])
    totals.append(["", "", "", "", "GRAND TOTAL", f"₹ {total_amount:.2f}"])

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
