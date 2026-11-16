"""HTTP API for the Industrial Diagnostics Assistant."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .diagnostics import analyse_readings, rule_reference

app = FastAPI(
    title="Industrial Diagnostics Assistant",
    description="Explainable first-line checks for industrial sensor readings.",
    version="0.1.0",
)


class SensorReadings(BaseModel):
    temperature_c: float = Field(ge=-20, le=250, description="Motor temperature in °C")
    vibration_mm_s: float = Field(ge=0, le=100, description="Vibration velocity in mm/s")
    pressure_bar: float = Field(ge=0, le=50, description="Operating pressure in bar")


@app.get("/health")
def health():
    return {"status": "ok", "service": "industrial-diagnostics-assistant"}


@app.get("/rules")
def rules():
    return {"rules": rule_reference()}


@app.post("/analyse")
def analyse(payload: SensorReadings):
    try:
        return analyse_readings(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/")
def home():
    return {
        "message": "Industrial Diagnostics Assistant API",
        "docs": "/docs",
        "example": {
            "temperature_c": 82.0,
            "vibration_mm_s": 3.1,
            "pressure_bar": 5.2,
        },
    }
