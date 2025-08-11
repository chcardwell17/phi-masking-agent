# 🩺 PHI Masking Agent

The **PHI Masking Agent** is a locally running AI-powered application that takes sample clinical notes and masks all Protected Health Information (PHI) such as patient names, dates of birth, contact details, and other identifiable elements.  
It runs on **Streamlit** with an integrated local **Ollama LLM** backend for privacy-preserving processing, and can optionally be monitored with Langfuse.

---

## 🚀 Features
- Upload or use sample clinical notes.
- Automatically detect and mask PHI entities.
- Run entirely **locally** for maximum data privacy.
- GPU acceleration via Ollama for LLM inference.
- Simple web UI built with Streamlit.

---

## 🛠️ Installation & Setup

### 1️⃣ Install Dependencies
Make sure you have [Homebrew](https://brew.sh/) installed.

Install Ollama:
```bash
brew install ollama
```

### 2️⃣ Install the LLM Model
Pull the Qwen 3 4B parameter model:
```bash
ollama pull qwen3:4b
```

> This model runs locally and requires sufficient VRAM (4GB+ recommended).

---

### 3️⃣ Set Up Conda Environment
Make sure you have [conda](https://docs.conda.io/en/latest/) installed.

Create and activate the environment from the `requirements.env` file:
```bash
conda env update -f ./environment.yml
conda activate phi_masking_agent_env
```

---

### 4️⃣ Run the Streamlit App
The main application file is `phi_masking_agent.py`.

Run:
```bash
streamlit run phi_masking_agent.py
```

This will start the web UI at:
```
http://localhost:8501
```

---

## 📂 Project Structure
```
.
├── phi_masking_agent.py     # Main Streamlit application
├── requirements.env         # Conda environment file
├── sample_data/             # Example clinical notes CSV
└── README.md                # This documentation
```

---

## ⚙️ How It Works
1. Loads a sample clinical note from CSV.
2. Sends text to a locally running Ollama LLM (`qwen3:4b`).
3. Detects PHI elements (name, date, phone, ID, email, organization, etc.).
4. Returns the note with PHI replaced by masked placeholders.

---

## 📜 License
This project is licensed under the APACHE-2.0 License — see the LICENSE file for details.
