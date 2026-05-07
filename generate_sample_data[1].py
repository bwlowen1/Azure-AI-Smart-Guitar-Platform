
from pathlib import Path
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
import textwrap

Path('images').mkdir(exist_ok=True)
Path('invoices').mkdir(exist_ok=True)
Path('emails').mkdir(exist_ok=True)

# image
img = Image.new('RGB', (640, 480), 'burlywood')
d = ImageDraw.Draw(img)
d.rectangle([220, 150, 420, 350], outline='saddlebrown', width=6)
d.rectangle([300, 50, 340, 150], outline='saddlebrown', width=6)
d.rectangle([260, 220, 320, 250], outline='red', width=4)
img.save('images/guitar.png')

# invoice pdf
c = canvas.Canvas('invoices/invoice.pdf')
c.drawString(50, 800, 'Invoice ID: INV-2025-01')
c.drawString(50, 780, 'Supplier Lot: LOT-1234')
c.drawString(50, 760, 'Item: Bridge Assembly')
c.drawString(50, 740, 'Total: $149.99')
c.showPage()
c.save()

# email
email_text = """Subject: Warranty claim

Hi Support,
The bridge on my new guitar arrived loose and causes buzzing.
Please advise on replacement.

Thanks,
Concerned Customer
"""
Path('emails/email.txt').write_text(textwrap.dedent(email_text), encoding='utf-8')
print('Synthetic demo data generated.')
