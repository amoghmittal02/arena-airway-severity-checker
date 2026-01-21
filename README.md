# Arena Airway Severity Checker

An explainable clinical screening tool that estimates airway obstruction severity based on deviation from reference airway measurements.

This project implements a lightweight AI-assisted system using a deterministic severity engine, a FastAPI backend, and a Streamlit-based user interface designed for non-technical clinical users.

---

## 🫁 Problem Statement

Arena Healthcare required a tool that:
- Accepts airway measurements (airway size, air volume, optional BMI)
- Outputs a clinically interpretable severity level:
  - **Stage A**: Nasal obstruction
  - **Stage B**: Nasal obstruction + mouth breathing / bruxism
  - **Stage C**: Nasal obstruction + bruxism + obesity (most severe)
- Works with limited labeled data
- Is transparent and explainable

---

## 🧠 Approach & Design

### Why rule-based instead of ML?
The provided dataset contained ~50–60 rows with sparse and inconsistent severity labels.  
Training a supervised ML model would be statistically unreliable and clinically unsafe.

Instead, we implemented:
- A **deterministic severity engine** based on deviation from established normal reference values
- An AI-assisted UI layer that handles input validation, symptom flags, and explanation

This design is:
- Clinically interpretable
- Robust with small datasets
- Easily extensible to ML when more labeled data becomes available

---

## 📐 Reference Normals Used

| Metric       | Normal Reference |
|-------------|------------------|
| Airway      | ≥ 20 cc          |
| Air Volume  | ≥ 150 mm²        |
| Obesity     | BMI ≥ 30         |

---

## ⚙️ Severity Logic (High-Level)

1. **Obstruction Detection**
   - Obstruction present if airway < 20 OR air volume < 150

2. **Deviation Scoring**
   - Normalized deficit computed for airway and air volume
   - Combined into an obstruction severity score

3. **Stage Assignment**
   - **Stage C**: Obstruction + BMI ≥ 30
   - **Stage B**: Obstruction + mouth breathing / bruxism (or inferred via deviation proxy)
   - **Stage A**: Obstruction only
   - **Normal**: No obstruction

The system prefers **explicit symptom inputs** when available and falls back to deviation-based inference when symptoms are unknown.

---

## 🏗️ Architecture


- **Streamlit**: Non-technical UI with input fields and explanations
- **FastAPI**: API layer exposing `/severity`
- **Severity Engine**: Pure Python logic (testable & explainable)

---

## 🚀 Running the Project Locally

### 1. Setup virtual environment

- python -m venv .venv
- source .venv/bin/activate   # Windows: .venv\Scripts\activate
- pip install -r requirements.txt

### 2. Start API
- uvicorn app:app --reload --port 8000
- http://127.0.0.1:8000/docs

### 3. Start UI
- streamlit run ui_streamlit.py
- http://localhost:8501
