from cli.chat import _run_opgrip_measurement, _run_refractory_measurement


def test_opgrip_runs_on_python_engine_without_model():
    result = _run_opgrip_measurement("/nonexistent/model.clm", ["--opgrip"])

    assert result["mode"] == "cheap"
    assert result["ticks"] == 250
    assert result["decode"] is False
    assert result["positive_control_hamming"] == result["ticks"]
    assert result["instrument_live"] is True
    assert any(value > 0 for value in result["hamming"].values())


def test_refractory_measurement_exercises_recovery_window():
    result = _run_refractory_measurement()

    assert result["ticks"] == 200
    assert result["emitted"] > 0
    assert result["refractory_ticks"] > 0
    assert result["stateless_fires_in_window"] > 0
    assert result["refractory_violations"] == 0
    assert result["f1_not_hard_urgency_gate"] is True
    assert result["f2_recovery_after_firing"] is True
