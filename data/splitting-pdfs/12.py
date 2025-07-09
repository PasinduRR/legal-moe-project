from PyPDF2 import PdfReader, PdfWriter
import os

input_pdf = "12. Consumer Affairs Authority Act No 9 of 2003.pdf"

sections = [
    ("Short title and Establishment", 1),
    ("Objects and Functions of the Authority", 2),
    ("Regulation of Trade", 5),
    ("Standards and Specifications", 7),
    ("Complaints and Compensation", 8),
    ("Agreements and Price Control", 9),
    ("Promotion of Competition and Consumer Interest", 17),
    ("Consumer Affairs Council", 22),
    ("Fund of the Authority", 27),
    ("Financial Year and Audit", 28),
    ("Staff of the Authority", 29),
    ("General Provisions", 30),
    ("Offences and Penalties", 33),
    ("Regulations and Repeals", 42),
    ("Interpretation and Schedules", 47),
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
