# 📄 ContractIQ – User Guide

Welcome to **ContractIQ** – your smart AI-powered contract management tool.  
There are **two versions** of this app:

- 🖥️ **Desktop version** (Tkinter-based executable)  
- 🌐 **Python version** (Streamlit-based web app)

---

## 🖥️ Desktop Version (Tkinter)

### ✅ How to Use

1. **Create a Gemini API key**  
   Go to [Google AI Studio](https://makersuite.google.com/app/apikey) and generate a key.

2. **Edit the code**  
   Open:
   ```
   desktopVersion/fullStackTkinter.py
   ```
   Replace the `apiKey` variable with your key.

3. **Install Python 3.12**

4. **Build the executable**  
   Open Command Prompt in the `desktopVersion/` folder and run:

   ```bash
   pip install pyinstaller
   pyinstaller --onefile --add-data "contracts.json;." fullStackTkinter.py
   ```

5. **Run the app**  
   After the build is complete, navigate to:

   ```
   desktopVersion/dist/fullStackTkinter.exe
   ```

   You can now launch your standalone desktop app.

> This version uses the **CustomTkinter** library. You can also run the `.py` file directly.

---

## 🌐 Python Version (Streamlit)

### ✅ How to Use

1. **Create a Gemini API key**  
   Go to [Google AI Studio](https://makersuite.google.com/app/apikey) and generate a key.

2. **Edit the code**  
   Open:
   ```
   desktopVersion/fullStack.py
   ```
   Replace the `apiKey` variable with your key.

3. **Install Python 3.12**

4. **Run the app**  
   Open Command Prompt in the same folder and run:

   ```bash
   python fullStack.py
   ```

   It will launch in your browser using Streamlit.

---

## 🧠 App Features

Upon opening the app, you will find **four tabs**:

1. **Dashboard** – View all your current contracts at a glance  
2. **Add Contract** – Upload a contract PDF and let Gemini summarize it  
3. **View Contract** – Explore full details of each contract  
4. **TheLegalEagle** – Ask questions about your contract using AI  

---

📂 All contract data is saved in `contracts.json` and reused every time you run the app.

🔒 Your API key is not shared anywhere.

---

Enjoy using **ContractIQ**! 🦅✨
