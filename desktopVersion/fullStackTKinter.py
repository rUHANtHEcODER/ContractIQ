import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import pdfplumber
import json
import os
import re
import pycountry
import google.generativeai as genai

# ------------------ Configuration ------------------
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("System")

API_KEY = "AIzaSyA99rXwMfKPSHArGV2WjaOvmhXiYAmBo5w"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

contracts_file = "../contracts.json"
contracts_data = {"contracts": []}

if os.path.exists(contracts_file):
    try:
        with open(contracts_file, "r") as f:
            contracts_data = json.load(f)
    except:
        contracts_data = {"contracts": []}

# ------------------ Expander Frame ------------------
class ExpanderFrame(ctk.CTkFrame):
    def __init__(self, master, title="More Info", content="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.expanded = False
        self.content_text = content

        self.toggle_btn = ctk.CTkButton(self, text=f"▶ {title}", command=self.toggle)
        self.toggle_btn.pack(fill="x", padx=5, pady=(5, 0))

        self.content_box = ctk.CTkTextbox(self, wrap="word", height=100)
        self.content_box.insert("1.0", self.content_text)
        self.content_box.configure(state="disabled")  # Make it read-only
        self.content_box.pack(fill="x", padx=5, pady=5)
        self.content_box.forget()

    def toggle(self):
        if self.expanded:
            self.content_box.forget()
            self.toggle_btn.configure(text=self.toggle_btn.cget("text").replace("▼", "▶"))
        else:
            self.content_box.pack(fill="x", padx=5, pady=5)
            self.toggle_btn.configure(text=self.toggle_btn.cget("text").replace("▶", "▼"))
        self.expanded = not self.expanded

# ------------------ Core Functions ------------------
def save_contracts():
    with open(contracts_file, "w") as f:
        json.dump(contracts_data, f, indent=2)

def extract_text_from_pdf(filepath):
    with pdfplumber.open(filepath) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)

def summarize_contract(text):
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
Contract: {text}
"""
    response = model.generate_content(prompt, generation_config={"max_output_tokens": 2048})
    cleaned = re.sub(r"\*\*|\n\s*\n|\n|\s{2,}", " ", response.text)
    matches = re.findall(r"(\d\.\s[^:]+):\s*(.*?)(?=\s*\d\.|$)", cleaned)
    return {title.strip(): content.strip() for title, content in matches}

# ------------------ UI Setup ------------------
app = ctk.CTk()
app.title("ContractIQ")
app.geometry("1000x700")

tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

tab_dashboard = tabview.add("Dashboard")
tab_new = tabview.add("New Contract")
tab_view = tabview.add("View Contract")
tab_eagle = tabview.add("The Leagle Eagle")

# ------------------ Dashboard Tab ------------------
def refresh_dashboard():
    for widget in tab_dashboard.winfo_children():
        widget.destroy()

    if not contracts_data["contracts"]:
        ctk.CTkLabel(tab_dashboard, text="No contracts uploaded yet.", font=("Arial", 16)).pack(pady=20)
        return

    for idx, contract in enumerate(contracts_data["contracts"]):
        frame = ctk.CTkFrame(tab_dashboard)
        frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(frame, text=f"{contract['name']}", font=("Arial", 18, "bold")).pack(anchor="w", padx=10, pady=4)
        ctk.CTkLabel(frame, text=f"Parties: {contract['parties']}").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"Payment: {contract['payment']}").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"Deadlines: {contract['deadlines']}").pack(anchor="w", padx=10)
        ctk.CTkLabel(frame, text=f"Services: {contract['services']}").pack(anchor="w", padx=10)

        def mark_done(index=idx):
            contracts_data["contracts"].pop(index)
            save_contracts()
            refresh_dashboard()

        ctk.CTkButton(frame, text="✔ Mark as Done", command=mark_done).pack(anchor="e", padx=10, pady=5)

        details = f"""Duration: {contract['duration']}
Termination: {contract['termination']}
Ownership: {contract['ownership']}
Summary: {contract['summary']}"""

        expander = ExpanderFrame(frame, title="View Full Details", content=details)
        expander.pack(fill="x", padx=10, pady=5)

refresh_dashboard()

# ------------------ New Contract Tab ------------------
def add_new_contract():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return
    name = simpledialog.askstring("Contract Name", "Enter a name for the contract:")
    if not name:
        return

    text = extract_text_from_pdf(filepath)
    data = summarize_contract(text)
    contract_data = {
        "name": name,
        "parties": data.get("1. Parties Involved", "N/A"),
        "payment": data.get("2. Amount / Payment Terms", "N/A"),
        "deadlines": data.get("3. Deadlines / Delivery Dates", "N/A"),
        "services": data.get("4. Services / Obligations", "N/A"),
        "duration": data.get("5. Duration (Start and End Date)", "N/A"),
        "termination": data.get("6. Termination Clause", "N/A"),
        "ownership": data.get("7. Ownership / Rights", "N/A"),
        "summary": data.get("8. Summary (1-2 lines)", "N/A"),
    }

    contracts_data["contracts"].append(contract_data)
    save_contracts()
    messagebox.showinfo("Done", "Contract added successfully!")
    refresh_dashboard()

ctk.CTkButton(tab_new, text="Upload & Add Contract PDF", command=add_new_contract).pack(pady=30)

# ------------------ View Contract Tab ------------------
def view_contract_text():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if filepath:
        text = extract_text_from_pdf(filepath)
        win = ctk.CTkToplevel(app)
        win.title("Contract Viewer")
        win.geometry("800x600")
        textbox = ctk.CTkTextbox(win, wrap="word")
        textbox.insert("1.0", text)
        textbox.pack(expand=True, fill="both", padx=10, pady=10)

ctk.CTkButton(tab_view, text="View Contract PDF", command=view_contract_text).pack(pady=30)

# ------------------ The Leagle Eagle ------------------
def ask_question_on_contract():
    filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not filepath:
        return

    country = simpledialog.askstring("Country", "Enter your country:")
    party = simpledialog.askstring("Party", "What party are you:")
    question = simpledialog.askstring("Question", "Enter your legal question:")

    if not (country and party and question):
        return

    text = extract_text_from_pdf(filepath)
    prompt = f"""Hello, I will give you a contract and you have to answer my questions based upon the contract.
Country: {country}
Party: {party}
Question: {question}
Contract: {text}
"""
    response = model.generate_content(prompt)
    result = response.text

    win = ctk.CTkToplevel(app)
    win.title("Legal Answer")
    win.geometry("700x500")
    textbox = ctk.CTkTextbox(win, wrap="word")
    textbox.insert("1.0", result)
    textbox.pack(expand=True, fill="both", padx=10, pady=10)

ctk.CTkButton(tab_eagle, text="Ask About Contract", command=ask_question_on_contract).pack(pady=30)

# ------------------ Run App ------------------
app.mainloop()
