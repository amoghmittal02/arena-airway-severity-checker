# severity.py
from typing import Optional, Dict, Any

NORMAL_AIRWAY = 20.0
NORMAL_VOLUME = 150.0

def predict_severity(
    airway_cc: float,
    volume_mm2: float,
    bmi: Optional[float] = None,
    mouth_breathing: Optional[bool] = None,
    bruxism: Optional[bool] = None,
) -> Dict[str, Any]:
    airway_deficit = max(0.0, (NORMAL_AIRWAY - airway_cc) / NORMAL_AIRWAY)
    volume_deficit = max(0.0, (NORMAL_VOLUME - volume_mm2) / NORMAL_VOLUME)
    obstruction_score = 0.5 * airway_deficit + 0.5 * volume_deficit

    obstruction = (airway_cc < NORMAL_AIRWAY) or (volume_mm2 < NORMAL_VOLUME)
    obese = (bmi is not None) and (bmi >= 30)

    if not obstruction:
        return {
            "stage": "Normal",
            "label": "No nasal obstruction (at/above reference normals)",
            "obstruction_score": round(obstruction_score, 3),
            "airway_deficit_pct": round(100 * airway_deficit, 1),
            "volume_deficit_pct": round(100 * volume_deficit, 1),
        }

    # If symptoms are provided, use them (preferred)
    symptoms_known = (mouth_breathing is not None) or (bruxism is not None)
    has_symptoms = bool(mouth_breathing) or bool(bruxism)

    if obese:
        return {
            "stage": "C",
            "label": "Nasal obstruction, bruxism, and obese",
            "note": "Obesity inferred from BMI >= 30. Bruxism may be self-reported or inferred in future versions.",
            "obstruction_score": round(obstruction_score, 3),
            "airway_deficit_pct": round(100 * airway_deficit, 1),
            "volume_deficit_pct": round(100 * volume_deficit, 1),
        }

    if symptoms_known:
        if has_symptoms:
            return {
                "stage": "B",
                "label": "Nasal obstruction + mouth breathing/bruxism",
                "obstruction_score": round(obstruction_score, 3),
                "airway_deficit_pct": round(100 * airway_deficit, 1),
                "volume_deficit_pct": round(100 * volume_deficit, 1),
            }
        return {
            "stage": "A",
            "label": "Nasal obstruction",
            "obstruction_score": round(obstruction_score, 3),
            "airway_deficit_pct": round(100 * airway_deficit, 1),
            "volume_deficit_pct": round(100 * volume_deficit, 1),
        }

    # Proxy fallback (when symptoms missing)
    if obstruction_score >= 0.35:
        stage = "B"
        label = "Nasal obstruction + mouth breathing/bruxism (proxy from deviation)"
        note = "Symptoms not provided; B inferred from deviation-from-normal threshold."
    else:
        stage = "A"
        label = "Nasal obstruction"
        note = "Symptoms not provided; classified based on mild deviation."

    return {
        "stage": stage,
        "label": label,
        "note": note,
        "obstruction_score": round(obstruction_score, 3),
        "airway_deficit_pct": round(100 * airway_deficit, 1),
        "volume_deficit_pct": round(100 * volume_deficit, 1),
    }
