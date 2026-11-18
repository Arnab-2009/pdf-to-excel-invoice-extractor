"""
Automated PDF-to-Excel Invoice Extractor
----------------------------------------
Scans a directory of PDF invoices, parses structured fields using Regex,
and exports a formatted multi-tab Excel workbook with category summaries.
"""

import glob
import os
import re
import pdfplumber
import pandas as pd
from openpyxl.styles import Font, PatternFill


def extract_field(pattern: str, text: str, default: str = "N/A") -> str:
    """Safely extract a single regex capture group from raw PDF text."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default


def parse_invoice_pdf(pdf_path: str) -> dict:
    """Read a PDF file and return a dictionary of structured invoice fields."""
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    invoice_no = extract_field(r"Invoice Number:\s*([A-Z0-9-]+)", full_text)
    invoice_date = extract_field(r"Invoice Date:\s*(\d{4}-\d{2}-\d{2})", full_text)
    vendor = extract_field(r"Vendor:\s*(.+)", full_text)
    category = extract_field(r"Department Category:\s*(.+)", full_text)
    subtotal = float(extract_field(r"Subtotal:\s*\$([\d,]+\.\d{2})", full_text, "0.0").replace(",", ""))
    tax = float(extract_field(r"Tax.*?:\s*\$([\d,]+\.\d{2})", full_text, "0.0").replace(",", ""))
    total = float(extract_field(r"Grand Total:\s*\$([\d,]+\.\d{2})", full_text, "0.0").replace(",", ""))

    return {
        "Source File": os.path.basename(pdf_path),
        "Invoice No": invoice_no,
        "Date": invoice_date,
        "Vendor": vendor,
        "Category": category,
        "Subtotal ($)": subtotal,
        "Tax ($)": tax,
        "Grand Total ($)": total,
    }


def export_to_styled_excel(df: pd.DataFrame, output_path: str) -> None:
    """Write extracted invoices and category summary into a styled Excel workbook."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    summary_df = (
        df.groupby("Category", as_index=False)[["Subtotal ($)", "Tax ($)", "Grand Total ($)"]]
        .sum()
        .sort_values(by="Grand Total ($)", ascending=False)
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="All Invoices", index=False)
        summary_df.to_excel(writer, sheet_name="Category Summary", index=False)

        header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        for sheet_name in ["All Invoices", "Category Summary"]:
            ws = writer.sheets[sheet_name]
            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font

            for col in ws.columns:
                max_len = max(len(str(cell.value or "")) for cell in col) + 4
                ws.column_dimensions[col[0].column_letter].width = max_len


def main() -> None:
    pdf_files = sorted(glob.glob(os.path.join("sample_invoices", "*.pdf")))
    if not pdf_files:
        print("No PDFs found in ./sample_invoices/. Run generate_sample_invoices.py first.")
        return

    print(f"Found {len(pdf_files)} PDF invoices. Extracting structured data...")
    records = [parse_invoice_pdf(pdf_path) for pdf_path in pdf_files]
    df = pd.DataFrame(records)

    print("\n--- Extracted Invoice Preview ---")
    print(df.to_string(index=False))

    output_file = os.path.join("outputs", "consolidated_expenses.xlsx")
    export_to_styled_excel(df, output_file)
    print(f"\nExported formatted Excel report to ./{output_file}")


if __name__ == "__main__":
    main()