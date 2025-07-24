import pdfplumber
import google.generativeai as genai
import re

# Step 1: Extract text from PDF
with pdfplumber.open("SERVICE AGREEMENT.pdf") as pdf:
    full_text = ""
    for page in pdf.pages:
        full_text += page.extract_text() + "\n"

# Step 2: Configure Gemini
APIkey = ""
genai.configure(api_key=APIkey)
model = genai.GenerativeModel('gemini-2.5-flash')

# Step 3: Prompt for structured summary
prompt = f"""If I give you a contract, summarize it with the following structure.
Only use the format below. If a field is missing, write N/A.
1. Parties Involved:
2. Amount / Payment Terms:
3. Deadlines / Delivery Dates:
4. Services / Obligations:
5. Duration (Start and End Date):
6. Termination Clause:
7. Ownership / Rights:
8. Summary (1-2 lines):
Contract: {full_text}"""

response = model.generate_content(
    prompt,
    generation_config={"max_output_tokens": 2048}
)
result = response.text

# Step 4: Clean and parse Gemini output
# Remove bold markdown and fix weird line breaks
cleaned = re.sub(r"\*\*", "", result)               # remove bold markers
cleaned = re.sub(r"\n\s*\n", " ", cleaned)          # collapse double newlines
cleaned = re.sub(r"\n", " ", cleaned)               # remove all line breaks
cleaned = re.sub(r"\s{2,}", " ", cleaned)           # collapse multiple spaces

# Split into key-value pairs
matches = re.findall(r"(\d\.\s[^:]+):\s*(.*?)(?=\s*\d\.|$)", cleaned)
data = {title.strip(): content.strip() for title, content in matches}

# Step 5: Assign to variables
parties     = data.get("1. Parties Involved", "N/A")
payment     = data.get("2. Amount / Payment Terms", "N/A")
deadlines   = data.get("3. Deadlines / Delivery Dates", "N/A")
services    = data.get("4. Services / Obligations", "N/A")
duration    = data.get("5. Duration (Start and End Date)", "N/A")
termination = data.get("6. Termination Clause", "N/A")
ownership   = data.get("7. Ownership / Rights", "N/A")
summary     = data.get("8. Summary (1-2 lines)", "N/A")

# Step 6: Print results
print("\n--- Parsed Contract Data ---")
print("Parties:     ", parties)
print("Payment:     ", payment)
print("Deadlines:   ", deadlines)
print("Services:    ", services)
print("Duration:    ", duration)
print("Termination: ", termination)
print("Ownership:   ", ownership)
print("Summary:     ", summary)
