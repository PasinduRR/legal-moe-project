from PyPDF2 import PdfReader, PdfWriter
import os

input_pdf = "17. ElectronicTransactionActNo19of2006.pdf"

sections = [
    ("Short title and Objectives", 1),
    ("General Provisions", 1),
    ("Recognition of Data Messages and Other Communications", 2),
    ("Electronic Contracts", 6),
    ("Certification Authority and Certification Service Providers", 11),
    ("Rules Governing Evidence", 14),
    ("Miscellaneous", 15),
    ("Interpretation and Schedules", 18),
]

offset = 1

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
