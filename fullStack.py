import streamlit as st
import pdfplumber as pdr
import google.generativeai as genai
import os
import json
import re
import pycountry

# Set page layout and API key
st.set_page_config(page_title="ContractIQ", layout="wide")
APIkey = ""  # Replace with actual API key

# Title
st.title("ContractIQ")
st.subheader("Manage your contracts with perfection")

# Configure Gemini
genai.configure(api_key=APIkey)
model = genai.GenerativeModel('gemini-2.5-flash')

# Load existing contracts
contracts_data = {"contracts": []}
if os.path.exists("contracts.json"):
    try:
        with open("contracts.json", "r") as f:
            contracts_data = json.load(f)
    except json.JSONDecodeError:
        contracts_data = {"contracts": []}

# Tabs UI
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "New Contract", "View Contract", "The Leagle Eagle"])

# ---------------- Dashboard Tab ----------------
with tab1:
    st.caption("Dashboard")
    if contracts_data["contracts"]:
        for contract in contracts_data["contracts"]:
            with st.container(border = True):
                st.subheader(contract["name"])
                st.write(contract["parties"])
                st.write(contract["payment"])
                st.write(contract["deadlines"])
                st.write(contract["services"])
                if st.button("Mark as Done ✔️"):
                    contracts_data["contracts"].remove(contract)
                    with open("contracts.json", "w") as f:
                        json.dump(contracts_data, f, indent=2)
                    st.rerun()
                with st.expander("View Full"):
                    st.write(f"Name: {contract['name']}")
                    st.write(f"Parties: {contract['parties']}")
                    st.write(f"Payment: {contract['payment']}")
                    st.write(f"Deadlines: {contract['deadlines']}")
                    st.write(f"Services: {contract['services']}")
                    st.write(f"Duration: {contract['duration']}")
                    st.write(f"Termination: {contract['termination']}")
                    st.write(f"Ownership: {contract['ownership']}")
                    st.write(f"Summary: {contract['summary']}")
    else:
        st.info("No contracts uploaded yet.")

# ---------------- New Contract Tab ----------------
with tab2:
    st.caption("New Contract")
    file = st.file_uploader("Upload your contract PDF", type="pdf", key="NewContract")
    name = st.text_input("Please input a name for the contract")

    if file and name:
        st.caption("Contract Preview")
        st.write(file)
        if st.button("Add Contract"):
            with st.spinner("Processing contract..."):
                with pdr.open(file) as pdf:
                    full_text = ""
                    for page in pdf.pages:
                        full_text += page.extract_text() + "\n"

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
Contract: {full_text}
"""
                response = model.generate_content(prompt, generation_config={"max_output_tokens": 2048})
                result = response.text

                cleaned = re.sub(r"\*\*", "", result)
                cleaned = re.sub(r"\n\s*\n", " ", cleaned)
                cleaned = re.sub(r"\n", " ", cleaned)
                cleaned = re.sub(r"\s{2,}", " ", cleaned)

                matches = re.findall(r"(\d\.\s[^:]+):\s*(.*?)(?=\s*\d\.|$)", cleaned)
                data = {title.strip(): content.strip() for title, content in matches}

                contract_data = {
                    "name": name,
                    "parties": data.get("1. Parties Involved", "N/A"),
                    "payment": data.get("2. Amount / Payment Terms", "N/A"),
                    "deadlines": data.get("3. Deadlines / Delivery Dates", "N/A"),
                    "services": data.get("4. Services / Obligations", "N/A"),
                    "duration": data.get("5. Duration (Start and End Date)", "N/A"),
                    "termination": data.get("6. Termination Clause", "N/A"),
                    "ownership": data.get("7. Ownership / Rights", "N/A"),
                    "summary": data.get("8. Summary (1-2 lines)", "N/A")
                }

                contracts_data["contracts"].append(contract_data)
                with open("contracts.json", "w") as f:
                    json.dump(contracts_data, f, indent=2)

                st.success("Contract added successfully! Go to Dashboard tab to view it.")
                st.rerun()  # rerun to reflect update

with tab3:
    st.caption("View Contract")
    file = st.file_uploader("Upload your contract PDF", type="pdf", key="ViewContract")
    if file:
        if st.button("View Contract"):
            with st.spinner("Processing contract..."):
                with pdr.open(file) as pdf:
                    full_text = ""
                    for page in pdf.pages:
                        full_text += page.extract_text() + "\n"
                        st.write(full_text) 

with tab4:
    st.caption("The Leagle Eagle")
    file = st.file_uploader("Upload your contract PDF", type="pdf", key="EditContract")
    countries = sorted([country.name for country in pycountry.countries])
    country = st.selectbox("Select Country", countries)
    party = st.text_input("Please input what party you are:")
    question = st.text_input("Please input your question:")
    if file and country and party and question:
        if st.button("Ask about the contract"):
            with st.spinner("Processing contract..."):
                with pdr.open(file) as pdf:
                    full_text = ""
                    for page in pdf.pages:
                        full_text += page.extract_text() + "\n"
                prompt = f"""Hello, I will give you a contract and you have to answer my questions based upon the contract.
                Please refrain from saying anything such as 'Of course I can', or 'No I will not be able to do that' Only information from the contract.
                Here is some of my information to assist you in your task:
                Country: {country}
                Party: {party}
                Question: {question}
                Contract: {full_text}
                """
                response = model.generate_content(prompt)
                result = response.text
                st.write(result)
                        
