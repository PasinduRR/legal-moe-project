from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "10. Bills of Exchanger Ordinance.pdf"

# List of sections with their start pages (update as per the document's ToC)
# Only use the actual section names, not "PART I" etc.
sections = [
    ("Short title and Interpretation", 1),
    ("Preliminary", 2),
    ("Bills of Exchange", 3),
    ("Form and Interpretation", 3),
    ("Capacity and Authority of Parties", 7),
    ("The Consideration for a Bill", 9),
    ("Negotiation of Bills", 10),
    ("General Duties of the Holder", 13),
    ("Liabilities of Parties", 14),
    ("Discharges", 16),
    ("Acceptance and Payment for Honour", 17),
    ("Lost Instruments", 19),
    ("Bill in a Set", 20),
    ("Conflict of Laws", 21),
    ("Cheques on a Banker", 22),
    ("Crossed Cheques", 23),
    ("Promissory Notes", 24),
    ("Supplementary", 21),
    ("Schedule", 22)
]

# Offset between printed page numbers and PDF page indices
# Set to 0 if PDF and printed page numbers match
offset = 0

# Load the PDF document
reader = PdfReader(input_pdf)
total_pages = len(reader.pages)

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

    # Calculate the real end page
    if i + 1 < len(sections):
        real_end = sections[i + 1][1] + offset
    else:
        real_end = total_pages

    # Safety check: ensure real_end doesn't exceed total pages
    if real_end > total_pages:
        print(f"⚠️ Warning: Section '{title}' end page ({real_end}) exceeds total pages ({total_pages}). Clipping to last page.")
        real_end = total_pages

    # Add pages from real_start to real_end (inclusive)
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
