from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "09. Sale of goods part 1 5-1-2020 notes.pdf"

# Reduced main sections with their start pages (update as needed after reviewing the PDF)
sections = [
    ("Introduction and Contract for Sale of Goods", 1),
    ("What are 'Goods' and Consideration", 2),
    ("Capacity to Buy and Sell", 2),
    ("Formalities and Subject Matter", 2),
    ("Implied Conditions and Warranties", 3),
    ("Transfer of Property and Title", 5),
    ("Performance and Delivery", 6),
    ("Rights of Unpaid Seller", 7),
    ("Actions for Breach of Contract", 8),
]

# Offset: number of pages before printed page 1 (set to 0 if first page is page 1)
offset = 0

reader = PdfReader(input_pdf)
total_pages = len(reader.pages)

base_name = os.path.splitext(os.path.basename(input_pdf))[0]
output_dir = os.path.join(os.getcwd(), base_name)
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Output folder: {output_dir}")
print(f"📄 Using offset: {offset} | Total PDF pages: {total_pages}")

for i, (title, start) in enumerate(sections):
    writer = PdfWriter()
    real_start = start + offset

    # End page is one less than the next section's start, or last page of PDF
    if i + 1 < len(sections):
        next_start = sections[i + 1][1] + offset
        real_end = next_start
    else:
        real_end = total_pages

    if real_start <= real_end:
        for page_num in range(real_start - 1, real_end):
            writer.add_page(reader.pages[page_num])

        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        output_filename = f"{safe_title}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as out_file:
            writer.write(out_file)

        print(f"✅ Saved: {output_filename}")
    else:
        print(f"⚠️ Skipping section '{title}' because start > end ({real_start} > {real_end})")

print("🎉 Done splitting PDF!")
