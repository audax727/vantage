import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

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
    
    # Header
    elements.append(Paragraph(f"<b>{store_name}</b> - {report_type} Business Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", normal))
    elements.append(Spacer(1, 20))
    
    # Section 1 – Executive Summary
    elements.append(Paragraph("1. Executive Summary", h2_style))
    for insight in ai_data.get("insights", []):
        elements.append(Paragraph(f"• {insight}", normal))
    elements.append(Spacer(1, 15))
    
    # Section 2 – Sales Performance
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
    
    # Section 3 – Inventory Alerts
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
    
    # Section 4 – Financial Snapshot
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
    
    # Section 5 – Recommended Actions
    elements.append(Paragraph("5. Recommended Actions", h2_style))
    for action in ai_data.get("priority_actions", []):
        urgency = str(action.get("urgency", "")).upper()
        color = "red" if urgency == "HIGH" else ("orange" if urgency == "WARNING" else "green")
        elements.append(Paragraph(f"<b><font color='{color}'>[{urgency}]</font> {action.get('title', '')}:</b> {action.get('description', '')}", normal))
        elements.append(Spacer(1, 5))
        
    # Footer
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'], alignment=1, fontSize=9, textColor=colors.gray
    )
    elements.append(Paragraph("Generated by Vantage Analytics Agent", footer_style))
        
    doc.build(elements)
    buffer.seek(0)
    return buffer
