from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "01. Companies Act No. 7 of 2007.pdf"

# List of sections with their start pages according to the Table of Contents (ToC)
# Only start pages are specified here. End pages will be calculated dynamically.
sections = [
    ("Short title and date of operation", 1),
    ("ESSENTIAL CHARACTERISTICS OF COMPANIES", 1),
    ("INCORPORATION OF COMPANIES", 2),
    ("COMPANY NAMES", 4),
    ("ARTICLES OF ASSOCIATION", 11),
    ("COMPANY CONTRACTS ETC.", 14),
    ("PRE-INCORPORATION CONTRACTS", 17),
    ("AUTHENTICATION OF DOCUMENTS BY COMPANY", 19),
    ("PRIVATE COMPANIES", 19),
    ("COMPANIES LIMITED BY GUARANTEE", 23),
    ("SHARES AND DEBENTURES", 26),
    ("SHAREHOLDERS AND THEIR RIGHTS AND OBLIGATIONS", 66),
    ("REGISTRATION OF CHARGES", 77),
    ("MANAGEMENT AND ADMINISTRATION", 87),
    ("AMALGAMATIONS", 190),
    ("COMPROMISES WITH CREDITORS", 201),
    ("APPROVAL OF ARRANGEMENTS, AMALGAMATIONS AND COMPROMISES BY COURT", 208),
    ("PROVISIONS RELATING TO OFFSHORE COMPANIES", 212),
    ("WINDING UP", 215),
    ("ADMINISTRATORS", 300),
    ("FLOATING CHARGES", 320),
    ("RECEIVERS AND MANAGERS", 330),
    ("REGISTRAR-GENERAL OF COMPANIES AND REGISTRATION", 359),
    ("APPLICATION OF ACT TO EXISTING COMPANIES", 368),
    ("OVERSEAS COMPANIES", 371),
    ("ADVISORY COMMISSION", 385),
    ("COMPANIES DISPUTES BOARD", 387),
    ("OFFENCES", 391),
    ("MISCELLANEOUS", 393),
    ("REPEALS AND AMENDMENTS", 414),
    ("FIRST SCHEDULE", 414),
    ("SECOND SCHEDULE", 433),
    ("THIRD SCHEDULE", 434),
    ("FOURTH SCHEDULE", 434),
    ("FIFTH SCHEDULE", 442),
    ("SIXTH SCHEDULE", 443),
    ("SEVENTH SCHEDULE", 443),
    ("EIGHTH SCHEDULE", 448),
    ("NINTH SCHEDULE", 449),
    ("TENTH SCHEDULE", 452),
    ("ELEVENTH SCHEDULE", 454),
    ("TWELFTH SCHEDULE", 456),
    ("THIRTEENTH SCHEDULE", 458),
]

# Offset between printed page numbers in the document and the actual PDF page index.
# For example, if printed page 1 corresponds to PDF page 29, then offset = 28
offset = 28  # Adjust this based on your specific PDF

# Load the PDF document
reader = PdfReader(input_pdf)
total_pages = len(reader.pages)  # Total pages in the PDF

# Create an output directory named after the input PDF (without extension)
base_name = os.path.splitext(os.path.basename(input_pdf))[0]
output_dir = os.path.join(os.getcwd(), base_name)
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Output folder: {output_dir}")
print(f"📄 Using offset: {offset} | Total PDF pages: {total_pages}")

# Loop over each section
for i, (title, start) in enumerate(sections):
    writer = PdfWriter()

    # Calculate the real start page in the PDF (accounting for offset)
    real_start = start + offset

    # Calculate the real end page:
    # For all except the last section, include the start page of the next section as well,
    # to capture any overlapping content.
    # For the last section, end at the last page of the PDF.
    if i + 1 < len(sections):
        real_end = sections[i + 1][1] + offset  # inclusive of next section's start page
    else:
        real_end = total_pages

    # Safety check: ensure real_end doesn't exceed total pages
    if real_end > total_pages:
        print(f"⚠️ Warning: Section '{title}' end page ({real_end}) exceeds total pages ({total_pages}). Clipping to last page.")
        real_end = total_pages

    # Add pages from real_start to real_end (inclusive)
    # PyPDF2 pages are zero-indexed, so subtract 1 from real_start
    for page_num in range(real_start - 1, real_end):
        writer.add_page(reader.pages[page_num])

    # Sanitize the section title to create a valid filename
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
    output_filename = f"{safe_title}.pdf"
    output_path = os.path.join(output_dir, output_filename)

    # Write the split PDF section to disk
    with open(output_path, "wb") as out_file:
        writer.write(out_file)

    print(f"✅ Saved: {output_filename}")

print("🎉 Done splitting PDF!")
