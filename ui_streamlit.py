# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000/severity"

# st.set_page_config(page_title="Arena Airway Severity", layout="centered")
# st.title("Arena Airway Severity Checker")

# st.caption("Enter measurements to estimate severity based on deviation from normal reference values.")

# with st.form("severity_form"):
#     airway = st.number_input("Airway (cc)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
#     volume = st.number_input("Air Volume (mm²)", min_value=0.0, max_value=1000.0, value=150.0, step=1.0)
#     bmi = st.number_input("BMI (optional)", min_value=0.0, max_value=80.0, value=0.0, step=0.1)
#     col1, col2 = st.columns(2)
#     with col1:
#         mouth_breathing = st.radio("Mouth breathing?", ["Unknown", "Yes", "No"], index=0)
#     with col2:
#         bruxism = st.radio("Bruxism (teeth grinding)?", ["Unknown", "Yes", "No"], index=0)

#     submitted = st.form_submit_button("Check severity")

# def yn_to_bool(x):
#     if x == "Yes": return True
#     if x == "No": return False
#     return None

# if submitted:
#     payload = {
#         "airway_cc": airway,
#         "volume_mm2": volume,
#         "bmi": (bmi if bmi > 0 else None),
#         "mouth_breathing": yn_to_bool(mouth_breathing),
#         "bruxism": yn_to_bool(bruxism),
#     }

#     try:
#         r = requests.post(API_URL, json=payload, timeout=10)
#         r.raise_for_status()
#         data = r.json()
#     except Exception as e:
#         st.error(f"API error: {e}")
#     else:
#         stage = data.get("stage")
#         label = data.get("label")

#         if stage == "C":
#             st.error(f"Severity: {stage} — {label}")
#         elif stage == "B":
#             st.warning(f"Severity: {stage} — {label}")
#         elif stage == "A":
#             st.info(f"Severity: {stage} — {label}")
#         else:
#             st.success(f"{label}")

#         st.subheader("Details")
#         st.write({
#             "Obstruction score": data.get("obstruction_score"),
#             "Airway deficit %": data.get("airway_deficit_pct"),
#             "Air volume deficit %": data.get("volume_deficit_pct"),
#             "Note": data.get("note", "")
#         })

#         st.caption("⚠️ Screening support only — not a clinical diagnosis.")

import os
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/severity"

# --- Page config ---
st.set_page_config(page_title="Arena Airway Severity Checker", page_icon="🫁", layout="centered")

# --- Header with logo (optional) ---
# Put your logo file at: ./assets/arena_logo.png (recommended)
LOGO_PATH = os.path.join("assets", "arena_logo.png")

col_logo, col_title = st.columns([2, 5], vertical_alignment="center")
with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        # If you don't have the file yet, comment this out or keep as a placeholder
        st.write("")

with col_title:
    st.title("Arena Airway Severity Checker")
    st.caption("Enter measurements to estimate severity based on deviation from normal reference values.")

# --- Reference normals (Change #1) ---
st.info(
    "Reference normals used:\n"
    "- Airway ≥ 20 cc\n"
    "- Air Volume ≥ 150 mm²\n"
    "- Obesity: BMI ≥ 30"
)

# --- Input form ---
with st.form("severity_form"):
    airway = st.number_input(
        "Airway (cc)",
        min_value=0.0,
        max_value=100.0,
        value=None,          # Change #2: force user to enter
        step=0.1,
        placeholder="e.g., 16.5"
    )
    volume = st.number_input(
        "Air Volume (mm²)",
        min_value=0.0,
        max_value=1000.0,
        value=None,          # Change #2: force user to enter
        step=1.0,
        placeholder="e.g., 120"
    )
    bmi = st.number_input(
        "BMI (optional)",
        min_value=0.0,
        max_value=80.0,
        value=None,          # allow empty
        step=0.1,
        placeholder="e.g., 27.4"
    )

    c1, c2 = st.columns(2)
    with c1:
        mouth_breathing = st.radio("Mouth breathing?", ["Unknown", "Yes", "No"], index=0)
    with c2:
        bruxism = st.radio("Bruxism (teeth grinding)?", ["Unknown", "Yes", "No"], index=0)

    submitted = st.form_submit_button("Check severity")

def yn_to_bool(x: str):
    if x == "Yes":
        return True
    if x == "No":
        return False
    return None

# --- Validate required inputs (Change #2) ---
if submitted:
    if airway is None or volume is None:
        st.warning("Please enter both **Airway** and **Air Volume** to continue.")
        st.stop()

    payload = {
        "airway_cc": float(airway),
        "volume_mm2": float(volume),
        "bmi": float(bmi) if bmi is not None else None,
        "mouth_breathing": yn_to_bool(mouth_breathing),
        "bruxism": yn_to_bool(bruxism),
    }

    try:
        r = requests.post(API_URL, json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        st.error(f"API error: {e}")
        st.stop()

    stage = data.get("stage")
    label = data.get("label")

    # --- Result banner ---
    if stage == "C":
        st.error(f"Severity: {stage} — {label}")
    elif stage == "B":
        st.warning(f"Severity: {stage} — {label}")
    elif stage == "A":
        st.info(f"Severity: {stage} — {label}")
    else:
        st.success(f"{label}")

    # --- Details ---
    st.subheader("Details")
    st.write(
        {
            "Obstruction score": data.get("obstruction_score"),
            "Airway deficit %": data.get("airway_deficit_pct"),
            "Air volume deficit %": data.get("volume_deficit_pct"),
            "Note": data.get("note", "")
        }
    )

    # --- Why this result? (Change #3) ---
    st.markdown("### Why this result?")
    if stage == "C":
        st.write(
            "• Airway and/or air volume are below normal reference values\n"
            "• BMI indicates obesity (≥ 30)\n"
            "• Combined factors place this in the highest severity group"
        )
    elif stage == "B":
        st.write(
            "• Nasal obstruction is present (airway < 20 and/or air volume < 150)\n"
            "• Classified as Stage B based on either symptom flags or deviation-from-normal (proxy if symptoms are Unknown)"
        )
    elif stage == "A":
        st.write(
            "• Nasal obstruction is present\n"
            "• No obesity factor (BMI < 30 or BMI not provided)\n"
            "• Lower deviation indicates Stage A rather than Stage B"
        )
    else:
        st.write("• Airway and air volume are within normal reference ranges")

    st.caption("⚠️ Screening support only — not a clinical diagnosis.")

