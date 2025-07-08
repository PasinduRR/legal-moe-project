from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "13. Intellectual_Property_Act_No_36_of_2003.pdf"

# Expanded main sections and a few more subsections with their actual PDF start pages
sections = [
    ("Short title and Administration", 1),
    ("Copyright", 3),
    ("Related Rights", 17),
    ("Industrial Designs", 31),
    ("Requirements and Procedure for Registration of Industrial Designs", 36),
    ("Duration, Rights, and Licensing of Industrial Designs", 41),
    ("Patents", 49),
    ("Patent Application and Procedure", 71),
    ("Patent Rights, Limitations, and Licensing", 85),
    ("Trademarks", 89),
    ("Unfair Competition", 137),
    ("Appellate Procedures", 143),
    ("Miscellaneous", 151),
    ("Schedules", 163),
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
        for page_num in range(real_start - 1, real_end):  # 0-based indexing
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
