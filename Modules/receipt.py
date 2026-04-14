
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
import io


def generate_pdf_receipt(filename, items, total, customer_name="Walk-in", payment_method="Cash"):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # ---------------- LOGO ----------------
    try:
        logo = Image("Assets\logo.png", width=80, height=50)
        content.append(logo)
    except:
        pass

    # ---------------- SHOP DETAILS ----------------
    content.append(Paragraph("<b>Baiskeli Centre</b>", styles["Title"]))
    content.append(Paragraph("Nairobi CBD", styles["Normal"]))
    content.append(Paragraph("Tel: 0712345678", styles["Normal"]))
    content.append(Spacer(1, 10))

    # ---------------- RECEIPT INFO ----------------
    content.append(Paragraph(f"Receipt No: {filename}", styles["Normal"]))
    content.append(Paragraph(f"Customer: {customer_name}", styles["Normal"]))
    content.append(Paragraph(f"Payment: {payment_method}", styles["Normal"]))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("<b>-----------------------------------</b>", styles["Normal"]))

    # ---------------- ITEMS ----------------
    for item in items:
        name = item["name"]
        qty = item["quantity"]
        price = item["price"]
        total_item = qty * price

        content.append(
            Paragraph(f"{name} x{qty} @ {price:.2f} = {total_item:.2f}", styles["Normal"])
        )

    content.append(Paragraph("<b>-----------------------------------</b>", styles["Normal"]))
    content.append(Spacer(1, 10))

    # ---------------- TOTAL ----------------
    content.append(Paragraph(f"<b>TOTAL: KES {total:.2f}</b>", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Thank you for shopping with us!", styles["Normal"]))

    doc.build(content)

    buffer.seek(0)
    return buffer