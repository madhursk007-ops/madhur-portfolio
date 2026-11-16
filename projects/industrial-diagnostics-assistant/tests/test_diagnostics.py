import pytest

from app.diagnostics import analyse_readings


def readings(**overrides):
    values = {
        "temperature_c": 62.0,
        "vibration_mm_s": 2.2,
        "pressure_bar": 5.4,
    }
    values.update(overrides)
    return values


def test_normal_machine_has_no_findings():
    result = analyse_readings(readings())
    assert result["status"] == "normal"
    assert result["finding_count"] == 0


def test_temperature_warning_is_explained():
    result = analyse_readings(readings(temperature_c=80.0))
    assert result["status"] == "warning"
    assert result["findings"][0]["sensor"] == "temperature_c"
    assert result["findings"][0]["threshold"] == 75.0
    assert result["findings"][0]["recommendation"]


def test_critical_vibration_sets_critical_status():
    result = analyse_readings(readings(vibration_mm_s=8.0))
    assert result["status"] == "critical"


def test_low_pressure_is_detected_in_reverse_direction():
    result = analyse_readings(readings(pressure_bar=2.0))
    assert result["findings"][0]["severity"] == "critical"


def test_missing_reading_is_rejected():
    values = readings()
    del values["pressure_bar"]
    with pytest.raises(ValueError, match="Missing sensor"):
        analyse_readings(values)
