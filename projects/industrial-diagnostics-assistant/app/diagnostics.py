"""Explainable diagnostic rules for a small industrial sensor system.

This first version deliberately uses transparent engineering rules rather than
claiming to train an opaque AI model. Each finding includes the measurements
and threshold that triggered it.
"""
from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Rule:
    sensor: str
    label: str
    warning: float
    critical: float
    unit: str
    advice: str


RULES = (
    Rule("temperature_c", "High motor temperature", 75.0, 90.0, "°C",
         "Check ventilation, bearing friction and recent load changes."),
    Rule("vibration_mm_s", "Excessive vibration", 4.5, 7.1, "mm/s",
         "Inspect alignment, mounting bolts and bearing condition."),
    Rule("pressure_bar", "Low operating pressure", 4.0, 2.5, "bar",
         "Inspect for leaks, blocked filters and pump performance."),
)


def analyse_readings(readings: dict[str, float]) -> dict[str, Any]:
    """Evaluate sensor readings and return explainable findings.

    Missing or non-numeric readings are rejected instead of silently ignored.
    """
    expected = {rule.sensor for rule in RULES}
    missing = sorted(expected - readings.keys())
    extra = sorted(readings.keys() - expected)
    if missing:
        raise ValueError(f"Missing sensor readings: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Unknown sensor readings: {', '.join(extra)}")

    findings = []
    for rule in RULES:
        value = float(readings[rule.sensor])
        if rule.sensor == "pressure_bar":
            severity = "critical" if value <= rule.critical else (
                "warning" if value < rule.warning else None
            )
            threshold = rule.critical if severity == "critical" else rule.warning
        else:
            severity = "critical" if value >= rule.critical else (
                "warning" if value >= rule.warning else None
            )
            threshold = rule.critical if severity == "critical" else rule.warning

        if severity:
            findings.append({
                "sensor": rule.sensor,
                "issue": rule.label,
                "value": value,
                "unit": rule.unit,
                "severity": severity,
                "threshold": threshold,
                "recommendation": rule.advice,
            })

    status = "critical" if any(f["severity"] == "critical" for f in findings) else (
        "warning" if findings else "normal"
    )
    return {
        "status": status,
        "finding_count": len(findings),
        "findings": findings,
        "method": "transparent_threshold_rules",
        "disclaimer": "Decision support only; verify findings with qualified personnel.",
    }


def rule_reference() -> list[dict[str, Any]]:
    """Expose the configured thresholds for transparency in the UI/API."""
    return [asdict(rule) for rule in RULES]
