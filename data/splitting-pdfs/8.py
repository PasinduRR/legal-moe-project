from PyPDF2 import PdfReader, PdfWriter
import os

# Input PDF filename
input_pdf = "08. INSOLVENTS [Cap.103 - Lanka Law.pdf"

# Example: Update these section titles and start pages based on your actual PDF
sections = [
    ("Short title and Preliminary", 1),
    ("Acts of Insolvency in General", 3),
    ("Proceedings Before Adjudication", 7),
    ("Adjudication and Securing Property", 10),
    ("Transactions with the Insolvent", 15),
    ("Appointment by the Court of Provisional Assignees", 18),
    ("Choice of Assignees and Their Rights and Duties", 20),
    ("Proof of Debts and Payments", 25),
    ("Audit and Money Belonging to the Insolvent Estate", 28),
    ("Dividends", 30),
    ("Allowances to the Insolvent", 32),
    ("Certificate of Conformity", 33),
    ("Arrangements by Deed", 35),
    ("Composition After Adjudication", 36),
    ("Evidence", 37),
    ("Offences and Miscellaneous", 38),
    ("Interpretation and Schedules", 39),
]

offset = 0  # Set to 0 if PDF page 1 is printed page 1

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
