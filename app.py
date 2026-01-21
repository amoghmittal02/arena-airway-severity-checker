# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from severity import predict_severity

app = FastAPI(title="Arena Airway Severity API")

class SeverityRequest(BaseModel):
    airway_cc: float
    volume_mm2: float
    bmi: Optional[float] = None
    mouth_breathing: Optional[bool] = None
    bruxism: Optional[bool] = None

@app.post("/severity")
def severity(req: SeverityRequest):
    return predict_severity(
        airway_cc=req.airway_cc,
        volume_mm2=req.volume_mm2,
        bmi=req.bmi,
        mouth_breathing=req.mouth_breathing,
        bruxism=req.bruxism,
    )
