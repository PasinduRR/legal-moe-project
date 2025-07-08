from PyPDF2 import PdfReader, PdfWriter
import os

input_pdf = "18. Foreign Exchange ACT NO 12 of 2017.pdf"

sections = [
    ("Short title and Implementation", 1),
    ("Authorized Dealers and Restricted Dealers", 2),
    ("Foreign Exchange or Foreign Assets", 3),
    ("Current Transactions", 4),
    ("Capital Transactions", 5),
    ("Regulation of Certain Transactions", 8),
    ("Guidelines and Directions", 9),
    ("Investigations", 10),
    ("Failure to Comply and Penalties", 11),
    ("Investigations and Inquiries", 12),
    ("Board of Inquiry", 13),
    ("Liability of Bodies Corporate", 14),
    ("Recovery of Sums Due", 15),
    ("Permissions and Consents", 16),
    ("Burden of Proof and Presumptions", 17),
    ("Admissibility of Documents", 19),
    ("Indemnity and Secrecy", 20),
    ("Preservation of Financial Stability", 22),
    ("Contracts and Obligations", 23),
    ("Penalties and Regulations", 24),
    ("Repeal, Savings and Interpretation", 25),
    ("Schedule", 29),
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
