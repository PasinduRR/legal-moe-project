from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "04. Banking Act 30_1988.pdf"

# Main sections with their start pages (update these based on your ToC or visual inspection)
sections = [
    ("Short title and date of operation", 6),
    ("Licensing of banks", 6),
    ("Application for a licence", 7),
    ("Companies and bodies corporate, incorporated outside Sri Lanka to remit currency to Sri Lanka", 10),
    ("Issue of licence", 11),
    ("Limits imposed on all licensed commercial banks", 11),
    ("Payment of licence fee", 11),
    ("Consequences of failure to commence business on the issue of a licence", 12),
    ("Directions of Board where notice of cancellation is issued", 13),
    ("Commercial bank to suspend business", 14),
    ("Approval of the Monetary Board necessary prior to carrying on certain transactions", 16),
    ("Capital requirements, reserve funds and maintenance of liquid assets", 23),
    ("Off-shore banking business", 26),
    ("Accounts, audit, information and inspection", 30),
    ("Disqualification for appointment as director, secretary, etc.", 35),
    ("Control over licensed commercial banks", 40),
    ("Liquidation of licensed commercial banks", 50),
    ("Licensed specialised banks", 58),
    ("General provisions", 71),
    ("Repeal and interpretation", 77),
    # Schedules (add as needed, based on your document)
    ("SCHEDULE I", 81),
    ("SCHEDULE II", 82),
    ("SCHEDULE III", 84),
    ("SCHEDULE IV", 85),
]

# Offset: number of pages before printed page 1
offset = 0  # Adjust if the PDF contains unnumbered intro pages before page 1

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
