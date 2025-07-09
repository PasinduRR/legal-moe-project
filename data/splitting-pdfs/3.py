from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "03. Inland Revenue (Amendment) Act No. 2 of 2025.pdf"

# Main sections with their start pages (update these based on your ToC or visual inspection)
sections = [
    ("Short title and date of operation", 1),
    ("Amendment of Section 150", 2),
    ("Amendment of the First Schedule", 3),
    ("Amendment of the Third Schedule", 6),
    ("Amendment of the Fifth Schedule", 7),
    ("Sinhala text to prevail in case of inconsistency", 8),
    # Add more sections if the Act contains additional main headings or schedules
]

# Offset: number of pages before printed page 1
offset = 1  # Adjust if the PDF contains unnumbered intro pages before page 1

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

    # Calculate the real end page (exclusive)
    if i + 1 < len(sections):
        real_end = sections[i + 1][1] + offset
    else:
        real_end = total_pages

    if real_end > total_pages:
        print(f"⚠️ Warning: Section '{title}' end page ({real_end}) exceeds total pages ({total_pages}). Clipping to last page.")
        real_end = total_pages

    for page_num in range(real_start - 1, real_end):
        writer.add_page(reader.pages[page_num])

    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
    output_filename = f"{safe_title}.pdf"
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "wb") as out_file:
        writer.write(out_file)

    print(f"✅ Saved: {output_filename}")

print("🎉 Done splitting PDF!")