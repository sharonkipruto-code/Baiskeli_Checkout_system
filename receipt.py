# # from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# # from reportlab.lib.styles import getSampleStyleSheet
# # from datetime import datetime

# # def generate_pdf_receipt(filename, cart, total, customer_name="Walk-in", currency="KES"):
# #     doc = SimpleDocTemplate(filename)
# #     styles = getSampleStyleSheet()
# #     elements = []

# #     # Logo
# #     try:
# #         logo = Image("logo.jpeg", width=100, height=50)
# #         elements.append(logo)
# #     except:
# #         pass

# #     elements.append(Spacer(1, 10))

# #     # Shop Name
# #     elements.append(Paragraph("<b>Baiskeli Centre</b>", styles["Title"]))
# #     elements.append(Spacer(1, 10))

# #     # Customer + Date
# #     elements.append(Paragraph(f"<b>Customer:</b> {customer_name}", styles["Normal"]))
# #     elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
# #     elements.append(Spacer(1, 10))

# #     # Items
# #     elements.append(Paragraph("<b>Items</b>", styles["Heading3"]))

# #     for item in cart:
# #         name = item["name"]
# #         qty = item["quantity"]
# #         price = item["price"]
# #         item_total = qty * price

# #         elements.append(
# #             Paragraph(f"{name} (x{qty}) - {currency} {item_total:.2f}", styles["Normal"])
# #         )

# #     elements.append(Spacer(1, 10))

# #     # Total
# #     elements.append(Paragraph(f"<b>TOTAL: {currency} {total:.2f}</b>", styles["Normal"]))

# #     elements.append(Spacer(1, 10))
# #     elements.append(Paragraph("Thank you for your purchase!", styles["Italic"]))

# #     doc.build(elements)

# #     return filename  # ✅ return file name

# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
# from datetime import datetime
# import io


# def generate_pdf_receipt(sale_id, items, total):
#     buffer = io.BytesIO()  # ✅ no file saving issues

#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()

#     content = []

#     content.append(Paragraph("🚲 Baiskeli Centre", styles["Title"]))
#     content.append(Paragraph("Nairobi CBD", styles["Normal"]))
#     content.append(Spacer(1, 10))

#     content.append(Paragraph(f"Receipt No: {sale_id}", styles["Normal"]))
#     content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
#     content.append(Spacer(1, 10))

#     for item in items:
#         line = f"{item['name']} x{item['quantity']} - KES {item['price'] * item['quantity']}"
#         content.append(Paragraph(line, styles["Normal"]))

#     content.append(Spacer(1, 10))
#     content.append(Paragraph(f"TOTAL: KES {total}", styles["Heading2"]))
#     content.append(Spacer(1, 20))
#     content.append(Paragraph("Thank you for your business!", styles["Normal"]))

#     doc.build(content)

#     buffer.seek(0)
#     return buffer

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
        logo = Image("logo.jpeg", width=80, height=50)
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