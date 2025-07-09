from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "16. Trust Ordinance.pdf"

# Main sections with their actual PDF start pages (for a 25-page document)
sections = [
    ("Preliminary", 1),
    ("Of the Creation of Trusts", 3),
    ("Of the Duties and Liabilities of Trustees", 6),
    ("Of the Rights and Powers of Trustees", 13),
    ("Of the Disabilities of Trustees", 17),
    ("Of the Rights and Liabilities of the Beneficiary", 18),
    ("Of Vacating the Office of Trustee", 20),
    ("Of the Extinction of Trusts", 22),
    ("Constructive Trusts", 23),
    ("Charitable Trusts", 24),
    ("Schedules", 25),
]

offset = 0  # Set to 0 if the first printed page is the first PDF page

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
