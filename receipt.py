from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime

def generate_pdf_receipt(sale_id, items, total):
    filename = f"receipt_{sale_id}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("🚲 Baiskeli Centre", styles["Title"]))
    content.append(Paragraph("Nairobi CBD", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Receipt Info
    content.append(Paragraph(f"Receipt No: {sale_id}", styles["Normal"]))
    content.append(Paragraph(f"Date: {datetime.now()}", styles["Normal"]))
    content.append(Spacer(1, 10))

    # Items
    for item in items:
        line = f"{item['name']} x{item['quantity']} - KES {item['price'] * item['quantity']}"
        content.append(Paragraph(line, styles["Normal"]))

    content.append(Spacer(1, 10))

    # Total
    content.append(Paragraph(f"TOTAL: KES {total}", styles["Heading2"]))

    content.append(Spacer(1, 20))
    content.append(Paragraph("Thank you for your business!", styles["Normal"]))

    doc.build(content)

    return filename