# pdf-to-excel-invoice-extractor
# 📄 Automated PDF-to-Excel Invoice Extractor

A Python automation pipeline that batch-processes unstructured PDF invoices, extracts key accounting fields using **pdfplumber** and **Regex**, and generates a formatted, multi-sheet Excel expense report with automated category rollups.

---

### 🎯 Problem Solved
Finance teams, freelancers, and small business owners frequently receive dozens of PDF invoices every month and manually copy totals into spreadsheets. This tool eliminates manual data entry—converting an entire folder of PDF receipts into an audit-ready Excel workbook in under 2 seconds.

---

### ⚙️ How It Works
1. **Batch PDF Ingestion:** Scans the `sample_invoices/` directory for all `.pdf` documents.
2. **Structured Field Parsing:** Extracts `Invoice No`, `Date`, `Vendor`, `Category`, `Subtotal`, `Tax`, and `Grand Total` using pattern-matched regular expressions.
3. **Automated Excel Reporting (`openpyxl`):**
   - **Sheet 1 (`All Invoices`):** Line-by-line consolidated ledger with source filename traceability.
   - **Sheet 2 (`Category Summary`):** Aggregated spend breakdown by department/category.
   - **Auto-Formatting:** Applies styled header banners and auto-adjusted column widths.

---

### 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Arnab-2009/pdf-to-excel-invoice-extractor.git](https://github.com/Arnab-2009/pdf-to-excel-invoice-extractor.git)
   cd pdf-to-excel-invoice-extractor