import re
import requests
import chainlit as cl

API_URL = "http://127.0.0.1:8000/severity"

def extract_float(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return float(m.group(1)) if m else None

@cl.on_message
async def main(message: cl.Message):
    text = message.content

    airway = extract_float(r"airway\s*[:=]?\s*([0-9]+(\.[0-9]+)?)", text)
    volume = extract_float(r"(volume|air\s*volume)\s*[:=]?\s*([0-9]+(\.[0-9]+)?)", text)
    bmi = extract_float(r"bmi\s*[:=]?\s*([0-9]+(\.[0-9]+)?)", text)

    # If user didn't format nicely, try: "20 150 28" style
    if airway is None or volume is None:
        nums = re.findall(r"\b\d+(\.\d+)?\b", text)
        nums = [float(x[0]) if isinstance(x, tuple) else float(x) for x in nums]
        if len(nums) >= 2 and airway is None and volume is None:
            airway, volume = nums[0], nums[1]
        if len(nums) >= 3 and bmi is None:
            bmi = nums[2]

    # Ask symptom questions only when obstruction is likely or inputs complete
    # For MVP: just ask if not provided in text
    mouth_breathing = None
    bruxism = None

    if airway is None or volume is None:
        await cl.Message(
            content="Send your measurements like:\n`airway: 17, air volume: 120, bmi: 29`\n(Optional: mouth_breathing: yes/no, bruxism: yes/no)"
        ).send()
        return

    payload = {
        "airway_cc": airway,
        "volume_mm2": volume,
        "bmi": bmi,
        "mouth_breathing": mouth_breathing,
        "bruxism": bruxism,
    }

    resp = requests.post(API_URL, json=payload, timeout=10)
    data = resp.json()

    explanation = f"""
**Severity:** {data.get("stage")}  
**Meaning:** {data.get("label")}  

**Deviation from normal**
- Airway deficit: {data.get("airway_deficit_pct")}%
- Air volume deficit: {data.get("volume_deficit_pct")}%
- Obstruction score: {data.get("obstruction_score")}

{("**Note:** " + data["note"]) if "note" in data else ""}
"""

    await cl.Message(content=explanation.strip()).send()
