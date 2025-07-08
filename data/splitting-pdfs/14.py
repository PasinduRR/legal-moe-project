from PyPDF2 import PdfReader, PdfWriter
import os

input_pdf = "14. ARBITRATION-ACT No 11 of 1995.pdf"

sections = [
    ("Short title and Preliminary", 1),
    ("Arbitration Agreement", 2),
    ("Composition of the Arbitral Tribunal", 3),
    ("Jurisdiction of the Arbitral Tribunal", 5),
    ("Conduct of Arbitration Proceedings", 7),
    ("Awards", 10),
    ("Application to Courts Relating to Awards", 13),
    ("Proceedings Before the High Court", 18),
    ("General Provisions as to Arbitration", 20),
    ("General Provisions", 22),
]

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
