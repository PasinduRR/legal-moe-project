from PyPDF2 import PdfReader, PdfWriter
import os

# 📄 Input PDF file
input_pdf = "07. Securities and Exchange Commission of Sri Lanka.pdf"

# 📋 Sections with start pages from the Table of Contents
# (you only need to specify start pages)
sections = [
    ("Short title and Preliminary", 1),
    ("Securities and Exchange Commission of Sri Lanka", 2),
    ("Powers, Duties and Functions of the Commission", 7),
    ("Director-General and Staff of the Commission", 12),
    ("Markets and Market Institutions", 16),
    ("Exchanges", 16),
    ("Clearing House", 27),
    ("Central Depository", 45),
    ("General Provisions (Market Institutions)", 53),
    ("Issue of Securities", 65),
    ("Public Offer of Securities", 66),
    ("Market Intermediaries", 76),
    ("Protection of Clients’ Assets", 88),
    ("Trade in Unlisted Securities", 93),
    ("Establishment of a Recognised Market Operator", 94),
    ("Role of a Recognised Market Operator", 95),
    ("Market Misconduct", 98),
    ("Finance", 118),
    ("Fund to Provide Compensation to Investors", 120),
    ("Financial Year and Audit of Accounts", 122),
    ("General", 122),
    ("Provisions Relating to Implementation", 123),
    ("Provisions Relating to Punishments and Enforcement Mechanisms", 133),
    ("Schedules", 166),
]

# 📄 Offset: if the PDF has e.g. 9 pages of cover/TOC before printed page 1
offset = 9

# 🔍 Load the PDF
reader = PdfReader(input_pdf)
total_pages = len(reader.pages)

# 📁 Output folder — named after the PDF file
base_name = os.path.splitext(os.path.basename(input_pdf))[0]
output_dir = os.path.join(os.getcwd(), base_name)
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Output folder: {output_dir}")
print(f"📄 Using offset: {offset} | Total PDF pages: {total_pages}")

# 🚀 Loop through each section
for i, (title, start) in enumerate(sections):
    writer = PdfWriter()
    real_start = start + offset

    # 📄 End page: include next section's start page
    if i + 1 < len(sections):
        next_start = sections[i + 1][1] + offset
        real_end = next_start  # include the next section's first page
    else:
        real_end = total_pages  # for the last section, go to end of PDF

    # 🧹 Safety check: clamp end page if it exceeds total pages
    if real_end > total_pages:
        print(f"⚠️ Warning: Section '{title}' end page ({real_end}) exceeds total pages ({total_pages}). Clipping to last page.")
        real_end = total_pages

    # 📝 Add pages to the writer
    if real_start <= real_end:
        for page_num in range(real_start - 1, real_end):  # 0-based indexing
            writer.add_page(reader.pages[page_num])

        # 🔐 Sanitize the filename
        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        output_filename = f"{safe_title}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        # 💾 Write the PDF section
        with open(output_path, "wb") as out_file:
            writer.write(out_file)

        print(f"✅ Saved: {output_filename}")
    else:
        print(f"⚠️ Skipping section '{title}' because start > end ({real_start} > {real_end})")

print("🎉 Done splitting PDF!")