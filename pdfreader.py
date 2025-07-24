import pdfplumber

with pdfplumber.open("SERVICE AGREEMENT.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print("TABLE ROW:", row)

print(full_text)
