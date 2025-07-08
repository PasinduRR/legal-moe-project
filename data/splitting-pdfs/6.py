from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "06. Banking (Special Provisions) Act, No. 17 of 2023.pdf"

# Main sections with their start pages (update as needed)
sections = [
    ("Preliminary", 1),
    ("Resolution Authority of the Central Bank", 2),
    ("Resolution Measures", 21),
    ("Sri Lanka Deposit Insurance Scheme", 39),
    ("Financial Sector Crisis Management Committee", 58),
    ("Winding Up of Licensed Bank", 65),
    ("Offences and Miscellaneous", 89),
    ("Interpretation and Schedules", 93),
]

# Offset: number of pages before printed page 1
offset = 1 # Adjust if the PDF contains unnumbered intro pages before page 1

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
        real_end = next_start - 1
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

print("🎉 Done splitting PDF!")