from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "05. Banking_Amendment_Act_No_24_of_2024_e.pdf"

# Logically grouped sections with their start pages (adjust as needed)
sections = [
    # 1. Preliminary
    ("Preliminary", 1),

    # 2. Licensing and Eligibility Amendments
    ("Licensing and Eligibility Amendments", 2),

    # 3. Regulatory and Supervisory Provisions
    ("Regulatory and Supervisory Provisions", 5),

    # 4. Accounts, Audit, and Disclosure
    ("Accounts, Audit, and Disclosure", 15),

    # 5. Governance and Management
    ("Governance and Management", 21),

    # 6. Prudential and Operational Controls
    ("Prudential and Operational Controls", 25),

    # 7. Winding Up and Liquidation
    ("Winding Up and Liquidation", 29),

    # 8. Specialized Banking Provisions
    ("Specialized Banking Provisions", 31),

    # 9. Penalties, Enforcement, and Miscellaneous
    ("Penalties, Enforcement, and Miscellaneous", 34),

    # 10. Schedules and Special Provisions
    ("Schedules and Special Provisions", 40),
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

    # End page is one less than the next section's start, or last page of PDF
    if i + 1 < len(sections):
        next_start = sections[i + 1][1] + offset
        real_end = next_start - 1
    else:
        real_end = total_pages

    # Only create a file if the range is valid
    if real_start <= real_end:
        for page_num in range(real_start - 1, real_end):
            writer.add_page(reader.pages[page_num])

        safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)
        output_filename = f"{safe_title}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as out_file:
            writer.write(out_file)

        print(f"✅ Saved: {output_filename}")

print("🎉 Done splitting PDF!")
