"""
Sample PDF Invoice Generator
----------------------------
Creates 5 realistic PDF invoices in ./sample_invoices/ so the extraction pipeline
can be tested and demonstrated out-of-the-box.
"""

import os
from fpdf import FPDF


SAMPLE_DATA = [
    {
        "filename": "INV_2026_001.pdf",
        "invoice_no": "INV-2026-001",
        "date": "2026-10-12",
        "vendor": "Apex Cloud Solutions",
        "category": "Cloud Hosting",
        "subtotal": "450.00",
        "tax": "81.00",
        "total": "531.00",
    },
    {
        "filename": "INV_2026_002.pdf",
        "invoice_no": "INV-2026-002",
        "date": "2026-10-18",
        "vendor": "Metro Office Supplies",
        "category": "Operations",
        "subtotal": "210.50",
        "tax": "37.89",
        "total": "248.39",
    },
    {
        "filename": "INV_2026_003.pdf",
        "invoice_no": "INV-2026-003",
        "date": "2026-10-25",
        "vendor": "Veloce Logistics Ltd",
        "category": "Shipping",
        "subtotal": "890.00",
        "tax": "160.20",
        "total": "1050.20",
    },
    {
        "filename": "INV_2026_004.pdf",
        "invoice_no": "INV-2026-004",
        "date": "2026-11-03",
        "vendor": "PixelCraft Media",
        "category": "Marketing",
        "subtotal": "600.00",
        "tax": "108.00",
        "total": "708.00",
    },
    {
        "filename": "INV_2026_005.pdf",
        "invoice_no": "INV-2026-005",
        "date": "2026-11-11",
        "vendor": "Apex Cloud Solutions",
        "category": "Cloud Hosting",
        "subtotal": "475.00",
        "tax": "85.50",
        "total": "560.50",
    },
]


def create_invoices(output_dir: str = "sample_invoices") -> None:
    os.makedirs(output_dir, exist_ok=True)

    for item in SAMPLE_DATA:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "TAX INVOICE", new_x="LMARGIN", new_y="NEXT")

        pdf.set_font("Helvetica", "", 11)
        pdf.ln(4)
        pdf.cell(0, 8, f"Vendor: {item['vendor']}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Invoice Number: {item['invoice_no']}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Invoice Date: {item['date']}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Department Category: {item['category']}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)
        pdf.cell(0, 8, f"Subtotal: ${item['subtotal']}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Tax (18%): ${item['tax']}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, f"Grand Total: ${item['total']}", new_x="LMARGIN", new_y="NEXT")

        filepath = os.path.join(output_dir, item["filename"])
        pdf.output(filepath)

    print(f"Generated {len(SAMPLE_DATA)} sample PDF invoices in ./{output_dir}/")


if __name__ == "__main__":
    create_invoices()