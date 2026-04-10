from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf_receipt(filename, cart, total, customer_name="Walk-in", currency="KES"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    # Logo
    try:
        logo = Image("logo.jpeg", width=100, height=50)
        elements.append(logo)
    except:
        pass

    elements.append(Spacer(1, 10))

    # Shop Name
    elements.append(Paragraph("<b>Baiskeli Centre</b>", styles["Title"]))
    elements.append(Spacer(1, 10))

    # Customer + Date
    elements.append(Paragraph(f"<b>Customer:</b> {customer_name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Items
    elements.append(Paragraph("<b>Items</b>", styles["Heading3"]))

    for item in cart:
        name = item["name"]
        qty = item["quantity"]
        price = item["price"]
        item_total = qty * price

        elements.append(
            Paragraph(f"{name} (x{qty}) - {currency} {item_total:.2f}", styles["Normal"])
        )

    elements.append(Spacer(1, 10))

    # Total
    elements.append(Paragraph(f"<b>TOTAL: {currency} {total:.2f}</b>", styles["Normal"]))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Thank you for your purchase!", styles["Italic"]))

    doc.build(elements)

    return filename  # ✅ return file name