from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "02. Inland Revenue Act_No_24_2017_E.pdf"

# Main subsections with their start pages (from ToC)
sections = [
    ("Short title and the effective date of the Act.", 1),
    ("IMPOSITION OF INCOME TAX", 1),
    ("INCOME TAX BASE", 2),
    ("CALCULATION OF THE INCOME TAX", 16),
    ("ASSETS AND LIABILITIES", 31),
    ("TYPES OF PERSONS", 43),
    ("SPECIAL INDUSTRIES", 53),
    ("INTERNATIONAL", 57),
    ("TAX PAYMENT PROCEDURE", 77),
    ("ADMINISTRATION PROVISIONS", 92),
    ("RECORD KEEPING AND INFORMATION COLLECTION", 109),
    ("TAX RETURNS", 118),
    ("ASSESSMENTS", 120),
    ("OBJECTIONS AND APPEALS", 127),
    ("LIABILITY FOR AND PAYMENT OF TAX", 131),
    ("INTEREST", 141),
    ("RECOVERY OF TAX", 143),
    ("PENALTIES", 158),
    ("CRIMINAL PROCEEDINGS", 164),
    ("REGULATIONS", 169),
    ("INTERPRETATION", 170),
    ("SPECIAL PROVISIONS", 195),
    ("TEMPORARY CONCESSIONS AND TRANSITIONAL PROVISIONS", 196),
    # Schedules
    ("FIRST SCHEDULE", 200),
    ("SECOND SCHEDULE", 207),
    ("THIRD SCHEDULE", 210),
    ("FOURTH SCHEDULE", 214),
    ("FIFTH SCHEDULE", 217),
    ("SIXTH SCHEDULE", 219),
]

# Offset: number of pages before printed page 1
offset = 12  # Adjust if printed page 1 is not PDF page 10

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
