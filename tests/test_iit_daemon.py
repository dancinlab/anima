import hashlib
import json
import os
import sys

import pytest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, "core")
if CORE not in sys.path:
    sys.path.insert(0, CORE)

import iit_daemon as ID
import generator as GEN
import recurrent_lane as RL
from cli import evaluate


def test_canonical_iit_controls_and_causal_cuts():
    canonical = RL.xor_ring_tpm()
    assert len(RL.validate_tpm(canonical)) == 24
    assert RL.mean_big_phi(canonical) == pytest.approx(2.25, abs=1e-6)
    assert RL.mean_big_phi(RL.independent_copy_tpm()) == pytest.approx(0.0, abs=1e-6)
    assert RL.mean_big_phi(RL.feedforward_broadcast_tpm()) == pytest.approx(0.0, abs=1e-6)
    values = RL.all_state_big_phi(canonical)
    assert len(values) == 8
    assert min(values) > 0.0
    edges = RL.causal_edges(canonical)
    assert edges == [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
    for parent, target in edges:
        assert RL.mean_big_phi(RL.cut_edge_tpm(canonical, parent, target)) == pytest.approx(
            0.0, abs=1e-6)
    for mask in range(1, 8):
        assert RL.mean_big_phi(RL.lesion_tpm(canonical, mask)) == pytest.approx(0.0, abs=1e-6)


def test_daemon_step_is_deterministic_but_intervention_sensitive():
    sequence = [1, 4, 2, 7]
    a = ID.IITDaemonCore(3)
    b = ID.IITDaemonCore(3)
    assert [a.step(x) for x in sequence] == [b.step(x) for x in sequence]
    assert ID.IITDaemonCore(3).step(0)["after"] != ID.IITDaemonCore(3).step(1)["after"]
    assert ID.IITDaemonCore(1).step(1, permutation=(0, 1, 2))["after"] != \
        ID.IITDaemonCore(1).step(1, permutation=(2, 1, 0))["after"]
    assert a.measure()["scope"] == "fixed-candidate-bounded-structure-loss"


@pytest.mark.parametrize("bad", [-1, 8, 1.0, True, "1"])
def test_daemon_rejects_invalid_state_and_intervention(bad):
    with pytest.raises((TypeError, ValueError)):
        ID.IITDaemonCore(bad)
    core = ID.IITDaemonCore()
    with pytest.raises((TypeError, ValueError)):
        core.step(bad)


@pytest.mark.parametrize("bad", [(0, 1), (0, 0, 2), (0, 1, 3), (0, 1, True), "012"])
def test_daemon_rejects_invalid_permutation(bad):
    with pytest.raises((TypeError, ValueError)):
        ID.IITDaemonCore().step(1, permutation=bad)


def test_snapshot_roundtrip_and_recovery(tmp_path):
    core = ID.IITDaemonCore(5)
    core.step(3)
    expected = core.snapshot()
    path = tmp_path / "state.json"
    core.save_snapshot(path)
    assert (path.stat().st_mode & 0o777) == 0o600
    core.step(6, lesion_mask=1)
    core.step(3, permutation=(2, 1, 0))
    assert core.snapshot() != expected
    restored = ID.IITDaemonCore.load_snapshot(path)
    assert restored.snapshot() == expected


def test_snapshot_corruption_and_schema_mismatch_fail_closed(tmp_path):
    path = tmp_path / "state.json"
    ID.IITDaemonCore(2).save_snapshot(path)
    document = json.loads(path.read_text())
    document["payload"]["state"] = 7
    path.write_text(json.dumps(document))
    with pytest.raises(ValueError, match="checksum"):
        ID.IITDaemonCore.load_snapshot(path)

    document = ID.IITDaemonCore(2).snapshot()
    document["schema"] = "unknown"
    path.write_text(json.dumps(document))
    with pytest.raises(ValueError, match="schema"):
        ID.IITDaemonCore.load_snapshot(path)


def _write_signed_snapshot(path, document):
    document["sha256"] = ID._sha256(document["payload"])
    path.write_text(json.dumps(document))


def test_snapshot_config_mismatch_and_out_of_range_state_fail_closed(tmp_path):
    path = tmp_path / "state.json"
    document = ID.IITDaemonCore(2).snapshot()
    document["payload"]["config_checksum"] = "0" * 64
    _write_signed_snapshot(path, document)
    with pytest.raises(ValueError, match="config checksum"):
        ID.IITDaemonCore.load_snapshot(path)

    document = ID.IITDaemonCore(2).snapshot()
    document["payload"]["state"] = 8
    _write_signed_snapshot(path, document)
    with pytest.raises(ValueError, match="state"):
        ID.IITDaemonCore.load_snapshot(path)


def test_snapshot_truncation_fails_closed(tmp_path):
    path = tmp_path / "state.json"
    ID.IITDaemonCore(2).save_snapshot(path)
    raw = path.read_bytes()
    path.write_bytes(raw[:len(raw) // 2])
    with pytest.raises(ValueError, match="canonical JSON"):
        ID.IITDaemonCore.load_snapshot(path)


def test_snapshot_refuses_oversize(tmp_path):
    path = tmp_path / "state.json"
    path.write_bytes(b"x" * (ID.MAX_SNAPSHOT_BYTES + 1))
    with pytest.raises(ValueError, match="size"):
        ID.IITDaemonCore.load_snapshot(path)


def test_tpm_validation_fails_closed():
    with pytest.raises(ValueError, match="needs"):
        RL.validate_tpm([0.0])
    with pytest.raises(ValueError, match="finite"):
        RL.validate_tpm([float("nan")] * 24)


def test_delayed_codebook_is_bijective_and_stable():
    cues = [0, 1, 2, 4]
    codebook = ID.delayed_codebook(cues)
    assert codebook == {0: 0, 6: 1, 5: 2, 3: 4}
    for state in codebook:
        assert ID.IITDaemonCore(state).step(0)["after"] == state


def test_delayed_task_normal_reset_and_address_shuffle():
    cues = [0, 1, 2, 4]
    delays = [1, 2, 4]
    normal = [ID.delayed_task_trial(cue, delay, cues)
              for cue in cues for delay in delays]
    reset = [ID.delayed_task_trial(cue, delay, cues, reset_every_turn=True)
             for cue in cues for delay in delays]
    shuffled = [ID.delayed_task_trial(cue, delay, cues, permutation=(1, 2, 0))
                for cue in cues for delay in delays]
    assert sum(trial["correct"] for trial in normal) == 12
    assert sum(trial["correct"] for trial in reset) == 3
    assert sum(trial["correct"] for trial in shuffled) == 3
    assert all(trial["reset_count"] == trial["delay"] for trial in reset)


@pytest.mark.parametrize("cues", [[], [0, 0], [0, 7], [0, 8]])
def test_delayed_task_rejects_invalid_codebook(cues):
    with pytest.raises((TypeError, ValueError)):
        ID.delayed_codebook(cues)


@pytest.mark.parametrize("delay", [0, -1, 1.0, True])
def test_delayed_task_rejects_invalid_delay(delay):
    with pytest.raises((TypeError, ValueError)):
        ID.delayed_task_trial(0, delay, [0, 1, 2, 4])


def test_clms_latch_uses_only_registered_prediction_as_bounded_cue():
    class_to_cue = {"good": 1, "bad": 2}
    assert ID.clms_latch_codebook(class_to_cue) == {6: "good", 5: "bad"}
    good = ID.clms_latch_trial("good", "good", class_to_cue)
    bad = ID.clms_latch_trial("bad", "bad", class_to_cue)
    assert good["action"] == "good" and good["correct"]
    assert bad["action"] == "bad" and bad["correct"]
    assert good["latch_cue"] == 1 and bad["latch_cue"] == 2
    assert good["mirrors_prediction"] and bad["mirrors_prediction"]


def test_iit_content_generator_reads_only_registered_final_state():
    codebook = {6: "good", 5: "bad"}
    surfaces = {"good": "The combined relation is good.",
                "bad": "The combined relation is bad."}
    assert GEN.gen_iit_state_content(6, codebook, surfaces) == {
        "state": 6, "class": "good", "text": surfaces["good"], "emitted": True}
    assert GEN.gen_iit_state_content(0, codebook, surfaces) == {
        "state": 0, "class": None, "text": "", "emitted": False}


def _workspace_records():
    return {
        "alpha": {"entity": "aria", "relation": "carries", "value": "ivory"},
        "beta": {"entity": "borin", "relation": "guards", "value": "amber"},
        "gamma": {"entity": "cyra", "relation": "observes", "value": "cedar"},
    }


def test_iit_workspace_selects_composable_record_from_final_state_only():
    cues = {"alpha": 1, "beta": 2, "gamma": 4}
    codebook = ID.content_workspace_codebook(cues)
    assert codebook == {6: "alpha", 5: "beta", 3: "gamma"}
    records = _workspace_records()
    selected = GEN.gen_iit_workspace_content(6, codebook, records)
    assert selected == {
        "state": 6, "address": "alpha", "record": records["alpha"],
        "text": "aria carries ivory.", "emitted": True,
    }
    assert GEN.gen_iit_workspace_content(0, codebook, records) == {
        "state": 0, "address": None, "record": None, "text": "", "emitted": False,
    }


def test_iit_workspace_reset_shuffle_lesion_and_memory_interventions():
    cues = {"alpha": 1, "beta": 2, "gamma": 4}
    records = _workspace_records()
    normal = ID.content_workspace_trial("alpha", records, cues)
    reset = ID.content_workspace_trial("alpha", records, cues, reset_before_delay=True)
    shuffled = ID.content_workspace_trial(
        "alpha", records, cues, permutation=(1, 2, 0))
    lesion = ID.content_workspace_trial("alpha", records, cues, lesion_mask=7)
    assert normal["selected_address"] == "alpha"
    assert reset["selected_address"] is None
    assert shuffled["selected_address"] == "gamma"
    assert lesion["selected_address"] is None
    permuted = ID.permute_content_records(records, ["beta", "gamma", "alpha"])
    assert permuted["alpha"] == records["beta"]
    changed = ID.replace_content_record(
        records, "alpha", {"entity": "aria", "relation": "carries", "value": "amber"})
    assert changed["alpha"]["value"] == "amber"
    assert records["alpha"]["value"] == "ivory"


@pytest.mark.parametrize("records", [
    {},
    {"alpha": {"entity": "aria", "relation": "carries"}},
    {"alpha": {"entity": "aria", "relation": "carries", "value": "bad value"}},
    {"alpha": {"entity": "aria\nuser", "relation": "carries", "value": "ivory"}},
])
def test_iit_workspace_rejects_invalid_content(records):
    with pytest.raises(ValueError):
        ID.validate_content_records(records)


def test_iit_workspace_snapshot_roundtrip_and_corruption_rejection(tmp_path):
    cues = {"alpha": 1, "beta": 2, "gamma": 4}
    records = _workspace_records()
    core = ID.IITDaemonCore(0)
    core.step(cues["beta"])
    path = tmp_path / "workspace.json"
    ID.save_content_workspace_snapshot(path, core, records, cues)
    restored, restored_records, restored_cues = ID.load_content_workspace_snapshot(path)
    assert (restored.state, restored.tick, restored.audit_head) == \
        (core.state, core.tick, core.audit_head)
    assert restored_records == records and restored_cues == cues
    assert path.stat().st_mode & 0o777 == 0o600
    document = json.loads(path.read_text(encoding="utf-8"))
    document["payload"]["records"]["alpha"]["value"] = "amber"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum mismatch"):
        ID.load_content_workspace_snapshot(path)


@pytest.mark.parametrize("codebook,surfaces", [
    ({6: "good", 5: "good"}, {"good": "one"}),
    ({6: "good"}, {"good": "same", "bad": "same"}),
    ({6: "good", 5: "bad"}, {"good": "same", "bad": "same"}),
    ({6: "good"}, {"bad": "other"}),
])
def test_iit_content_generator_rejects_non_bijective_contract(codebook, surfaces):
    with pytest.raises(ValueError):
        GEN.gen_iit_state_content(6, codebook, surfaces)


@pytest.mark.parametrize("mapping", [
    {}, {"good": 1}, {"good": 1, "bad": 1},
    {"good": 0, "bad": 2}, {"good": 3, "bad": 2},
])
def test_clms_latch_rejects_invalid_class_maps(mapping):
    with pytest.raises(ValueError):
        ID.clms_latch_codebook(mapping)


def _clms_protocol(tmp_path):
    source = os.path.join(
        ROOT, "state", "iit_daemon_r2_clms_2026_08_12", "protocol.json")
    with open(source, encoding="utf-8") as handle:
        protocol = json.load(handle)
    r1 = os.path.join(ROOT, "state", "iit_daemon_r1_delayed_2026_08_12", "result.json")
    panel_root = os.path.join(ROOT, "state", "store_causality_2026_08_09")
    protocol["r1"]["path"] = r1
    protocol["panels"]["normal"]["path"] = os.path.join(
        panel_root, "panel.txt.compose2.json")
    protocol["panels"]["drop_a"]["path"] = os.path.join(
        panel_root, "panel.txt.compose2_dropA.json")
    protocol["panels"]["drop_b"]["path"] = os.path.join(
        panel_root, "panel.txt.compose2_drop.json")
    checkpoint = tmp_path / "model.clm"
    checkpoint.write_bytes(b"pinned-r2-checkpoint")
    protocol["checkpoint"]["sha256"] = hashlib.sha256(
        checkpoint.read_bytes()).hexdigest()
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    return checkpoint, protocol_path


def _content_protocol(tmp_path, r2_document=None):
    source = os.path.join(
        ROOT, "state", "iit_daemon_r3_content_2026_08_12", "protocol.json")
    with open(source, encoding="utf-8") as handle:
        protocol = json.load(handle)
    if r2_document is None:
        r2_source = os.path.join(
            ROOT, "state", "iit_daemon_r2_clms_2026_08_12", "result.json")
        protocol["r2"]["path"] = r2_source
    else:
        r2_source = tmp_path / "r2.json"
        r2_source.write_text(json.dumps(r2_document), encoding="utf-8")
        protocol["r2"]["path"] = str(r2_source)
        protocol["r2"]["sha256"] = hashlib.sha256(r2_source.read_bytes()).hexdigest()
    protocol_path = tmp_path / "protocol-r3.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    return protocol_path


def _composition_protocol(tmp_path, mutate_panel=None):
    source_root = os.path.join(
        ROOT, "state", "iit_daemon_r35_workspace_2026_08_14")
    protocol = json.loads(open(os.path.join(source_root, "protocol.json"),
                               encoding="utf-8").read())
    panel = json.loads(open(os.path.join(source_root, "panel.json"),
                            encoding="utf-8").read())
    if mutate_panel is not None:
        mutate_panel(panel)
    panel_path = tmp_path / "panel-r35.json"
    panel_path.write_text(json.dumps(panel), encoding="utf-8")
    protocol["panel"] = {
        "path": str(panel_path),
        "sha256": hashlib.sha256(panel_path.read_bytes()).hexdigest(),
    }
    protocol["r3"]["path"] = os.path.join(
        ROOT, "state", "iit_daemon_r3_content_2026_08_12", "result.json")
    protocol_path = tmp_path / "protocol-r35.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    return protocol_path


def test_composition_evaluator_runs_registered_order_and_controls(tmp_path):
    protocol_path = _composition_protocol(tmp_path)
    out_path = tmp_path / "result-r35.json"
    rc = evaluate.iit_daemon_composition_run([
        "--iit-daemon-composition", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 0
    assert result["verdict"] == "SUPPORTED-COMPOSITIONAL-WORKSPACE-CAUSALITY"
    assert result["accuracies"] == {
        "oracle": 1.0, "normal": 1.0, "state_reset": 0.0,
        "iit_address_shuffled": 0.0, "workspace_address_shuffled": 0.0,
        "node_lesion": 0.0, "selected_memory_counterfactual": 1.0,
        "irrelevant_memory_mutation": 1.0, "recovery": 1.0,
    }
    assert all(result["checks"].values())
    assert all(row["differs_from_normal"]
               for row in result["arms"]["selected_memory_counterfactual"]["trials"])
    assert all(row["matches_normal"]
               for row in result["arms"]["irrelevant_memory_mutation"]["trials"])
    assert all(row["matches_normal"] for row in result["arms"]["recovery"]["trials"])


def test_composition_evaluator_oracle_failure_stops_later_arms(tmp_path, monkeypatch):
    protocol_path = _composition_protocol(tmp_path)
    out_path = tmp_path / "invalid-r35.json"
    original = evaluate.gen_runtime.gen_iit_workspace_content

    def broken_alpha(state, codebook, records):
        result = original(state, codebook, records)
        if result["address"] == "alpha":
            result = dict(result, text="broken oracle output.")
        return result

    monkeypatch.setattr(evaluate.gen_runtime, "gen_iit_workspace_content", broken_alpha)
    rc = evaluate.iit_daemon_composition_run([
        "--iit-daemon-composition", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 1 and result["verdict"] == "INVALID-INSTRUMENT"
    assert set(result["arms"]) == {"oracle"}


def test_composition_evaluator_rejects_panel_digest_mismatch(tmp_path):
    protocol_path = _composition_protocol(tmp_path)
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    protocol["panel"]["sha256"] = "0" * 64
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError, match="composition panel artifact mismatch"):
        evaluate.iit_daemon_composition_run([
            "--iit-daemon-composition", str(protocol_path)])


def test_content_evaluator_runs_registered_order_and_controls(tmp_path):
    protocol_path = _content_protocol(tmp_path)
    out_path = tmp_path / "result-r3.json"
    rc = evaluate.iit_daemon_content_run([
        "--iit-daemon-content", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 0
    assert result["verdict"] == "SUPPORTED-BOUNDED-CONTENT-CAUSALITY"
    assert result["accuracies"] == {
        "oracle_pair": 1.0, "normal": 0.953125, "state_reset": 0.0,
        "iit_address_shuffled": 0.0390625, "drop_a": 0.5,
        "drop_b": 0.4609375, "clms_address_shuffled": 0.46875,
        "recovery": 0.953125,
    }
    assert all(result["checks"].values())
    assert all(not row["emitted"]
               for row in result["content_arms"]["state_reset"]["trials"])
    assert all(row["matches_normal"]
               for row in result["content_arms"]["recovery"]["trials"])


def test_content_evaluator_pair_oracle_failure_stops_later_arms(tmp_path):
    r2_path = os.path.join(
        ROOT, "state", "iit_daemon_r2_clms_2026_08_12", "result.json")
    with open(r2_path, encoding="utf-8") as handle:
        r2 = json.load(handle)
    oracle = r2["latch_arms"]["oracle_pair"]
    for index, row in enumerate(oracle["trials"]):
        if index % 2:
            row["prediction"] = "bad" if row["gold"] == "good" else "good"
    oracle["accuracy"] = 0.5
    r2["latch_accuracies"]["oracle_pair"] = 0.5
    protocol_path = _content_protocol(tmp_path, r2)
    out_path = tmp_path / "invalid-r3.json"
    rc = evaluate.iit_daemon_content_run([
        "--iit-daemon-content", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 1
    assert result["verdict"] == "INVALID-INSTRUMENT"
    assert set(result["content_arms"]) == {"oracle_pair"}


def test_content_evaluator_rejects_r2_digest_mismatch(tmp_path):
    protocol_path = _content_protocol(tmp_path)
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    protocol["r2"]["sha256"] = "0" * 64
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError, match="R2 artifact mismatch"):
        evaluate.iit_daemon_content_run([
            "--iit-daemon-content", str(protocol_path)])


def _fake_clms_arm(argv, _return_result=False, _return_trials=False):
    path = argv[argv.index("--store") + 1]
    with open(path, encoding="utf-8") as handle:
        entries = json.load(handle)["entries"]
    positive = "--store-oracle-pair" in argv or (
        "compose2_drop" not in path and "--store-shuffle" not in argv)
    trials = []
    for index, item in enumerate(entries):
        gold = item["gold"]
        prediction = gold if positive or index % 2 == 0 else (
            "bad" if gold == "good" else "good")
        trials.append({"index": index, "prediction": prediction, "gold": gold,
                       "correct": prediction == gold})
    correct = sum(item["correct"] for item in trials)
    return {
        "arm": "oracle" if "--store-oracle-pair" in argv else "lookup",
        "oracle": "pair" if "--store-oracle-pair" in argv else False,
        "mode": "shuffle" if "--store-shuffle" in argv else "normal",
        "n": len(trials), "correct": correct,
        "accuracy": correct / float(len(trials)), "readable": len(trials),
        "shuffle_integrity": True, "trials": trials,
    }


def test_clms_latch_evaluator_runs_registered_order(tmp_path, monkeypatch):
    checkpoint, protocol_path = _clms_protocol(tmp_path)
    calls = []

    def fake(argv, _return_result=False, _return_trials=False):
        calls.append(list(argv))
        return _fake_clms_arm(argv, _return_result, _return_trials)

    monkeypatch.setattr(evaluate, "store_run", fake)
    out_path = tmp_path / "result.json"
    rc = evaluate.iit_daemon_clms_run([
        str(checkpoint), "--iit-daemon-clms", str(protocol_path),
        "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 0
    assert result["verdict"] == "SUPPORTED-CLMS-LATCH-CAUSALITY"
    assert result["latch_accuracies"] == {
        "oracle_pair": 1.0, "normal": 1.0, "drop_a": 0.5,
        "drop_b": 0.5, "address_shuffled": 0.5, "recovery": 1.0,
    }
    assert all(result["checks"].values())
    assert len(calls) == 6
    assert "--store-oracle-pair" in calls[0]
    assert "--store-shuffle" in calls[4]


def test_clms_latch_evaluator_stops_after_failed_oracle(tmp_path, monkeypatch):
    checkpoint, protocol_path = _clms_protocol(tmp_path)
    calls = []

    def dead_oracle(argv, _return_result=False, _return_trials=False):
        calls.append(list(argv))
        result = _fake_clms_arm(argv, _return_result, _return_trials)
        for index, trial in enumerate(result["trials"]):
            if index % 2:
                trial["prediction"] = "bad" if trial["gold"] == "good" else "good"
                trial["correct"] = False
        result["correct"] = sum(trial["correct"] for trial in result["trials"])
        result["accuracy"] = result["correct"] / float(result["n"])
        return result

    monkeypatch.setattr(evaluate, "store_run", dead_oracle)
    out_path = tmp_path / "result.json"
    rc = evaluate.iit_daemon_clms_run([
        str(checkpoint), "--iit-daemon-clms", str(protocol_path),
        "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 1
    assert result["verdict"] == "INVALID-INSTRUMENT"
    assert len(calls) == 1
    assert set(result["clms_arms"]) == {"oracle_pair"}


def test_clms_latch_evaluator_rejects_checkpoint_mismatch(tmp_path):
    checkpoint, protocol_path = _clms_protocol(tmp_path)
    checkpoint.write_bytes(b"changed-after-registration")
    with pytest.raises(ValueError, match="checkpoint checksum mismatch"):
        evaluate.iit_daemon_clms_run([
            str(checkpoint), "--iit-daemon-clms", str(protocol_path)])


def _delayed_protocol():
    path = os.path.join(
        ROOT, "state", "iit_daemon_r1_delayed_2026_08_12", "protocol.json")
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def test_delayed_evaluator_runs_registered_full_battery(tmp_path):
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(_delayed_protocol()), encoding="utf-8")
    out_path = tmp_path / "result.json"
    rc = evaluate.iit_daemon_delayed_run([
        "--iit-daemon-delayed", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 0
    assert result["verdict"] == "SUPPORTED-DELAYED-STATE-CAUSALITY"
    assert result["accuracies"] == {
        "normal": 1.0, "reset_every_turn": 0.25,
        "address_shuffled": 0.25, "recovery": 1.0,
    }
    assert all(result["checks"].values())


def test_delayed_evaluator_fails_closed_on_r0_fingerprint_change(tmp_path):
    protocol = _delayed_protocol()
    protocol["r0_mechanics_fingerprint"] = "0" * 64
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    out_path = tmp_path / "result.json"
    rc = evaluate.iit_daemon_delayed_run([
        "--iit-daemon-delayed", str(protocol_path), "--out", str(out_path)])
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert rc == 1
    assert result["verdict"] == "FALSIFIED"
    assert not result["checks"]["r0_mechanics_unchanged"]


def test_delayed_evaluator_rejects_miscalculated_chance(tmp_path):
    protocol = _delayed_protocol()
    protocol["chance"] = 0.5
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError, match="chance mismatch"):
        evaluate.iit_daemon_delayed_run([
            "--iit-daemon-delayed", str(protocol_path)])


@pytest.mark.parametrize("field,value", [
    ("positive_floor", float("nan")),
    ("control_margin", -0.01),
    ("engine", "other.engine"),
])
def test_delayed_evaluator_rejects_invalid_protocol_values(tmp_path, field, value):
    protocol = _delayed_protocol()
    protocol[field] = value
    protocol_path = tmp_path / "protocol.json"
    protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError):
        evaluate.iit_daemon_delayed_run([
            "--iit-daemon-delayed", str(protocol_path)])


def _semantic_bridge_examples():
    return [
        {"text": "Memory alpha: aria carries amber.", "labels": {
            "kind": "memory", "address": "alpha", "entity": "aria",
            "relation": "carries", "value": "amber"}},
        {"text": "Memory beta: borin guards cedar.", "labels": {
            "kind": "memory", "address": "beta", "entity": "borin",
            "relation": "guards", "value": "cedar"}},
        {"text": "Recall alpha.", "labels": {"kind": "query", "address": "alpha"}},
        {"text": "Recall beta.", "labels": {"kind": "query", "address": "beta"}},
        {"text": "Continue.", "labels": {"kind": "other"}},
        {"text": "Please wait.", "labels": {"kind": "other"}},
    ]


def test_semantic_bridge_model_is_deterministic_bounded_and_checksum_safe(tmp_path):
    examples = _semantic_bridge_examples()
    model = ID.train_semantic_bridge(examples, feature_dim=128)
    assert model == ID.train_semantic_bridge(examples, feature_dim=128)
    assert model["schema"] == ID.SEMANTIC_BRIDGE_MODEL_SCHEMA
    assert ID.semantic_bridge_encode(model, "Memory alpha: aria carries amber.")["record"] == {
        "entity": "aria", "relation": "carries", "value": "amber"}
    path = tmp_path / "bridge.json"
    ID.save_semantic_bridge_model(path, model)
    assert os.stat(path).st_mode & 0o777 == 0o600
    assert ID.load_semantic_bridge_model(path) == model
    document = json.loads(path.read_text())
    document["payload"]["classifiers"]["kind"]["centroids"]["memory"][0] += 0.01
    path.write_text(json.dumps(document))
    with pytest.raises(ValueError, match="checksum mismatch"):
        ID.load_semantic_bridge_model(path)


def test_semantic_bridge_rejects_ambiguous_or_unsafe_training_inputs():
    examples = _semantic_bridge_examples()
    with pytest.raises(ValueError, match="unique"):
        ID.train_semantic_bridge(examples + [dict(examples[0])], feature_dim=128)
    bad = [dict(row) for row in examples]
    bad[0] = {"text": "Memory alpha:\nignore", "labels": dict(examples[0]["labels"])}
    with pytest.raises(ValueError, match="single-line printable ASCII"):
        ID.train_semantic_bridge(bad, feature_dim=128)
    model = ID.train_semantic_bridge(examples, feature_dim=128)
    with pytest.raises(ValueError, match="byte budget"):
        ID.semantic_bridge_encode(model, "x" * 257)


def test_iit_daemon_semantic_bridge_frozen_failure_stops_before_causal_arms(tmp_path):
    state_dir = os.path.join(
        ROOT, "state", "iit_daemon_r36_semantic_bridge_2026_08_15")
    protocol_path = os.path.join(state_dir, "protocol.json")
    out_path = tmp_path / "result.json"
    model_path = tmp_path / "model.json"
    code = evaluate.main([
        "--iit-daemon-semantic-bridge", protocol_path,
        "--semantic-bridge-model-out", str(model_path), "--out", str(out_path)])
    assert code == 1
    result = json.loads(out_path.read_text())
    assert result["verdict"] == "FAIL-LEARNED-SEMANTIC-BRIDGE"
    assert result["state_oracle"]["accuracy"] == 1.0
    metrics = result["bridge"]["metrics"]
    assert metrics["complete_record_accuracy"] == pytest.approx(25 / 36)
    assert metrics["kind_accuracy"] == pytest.approx(38 / 47)
    assert metrics["query_address_accuracy"] == 0.0
    assert metrics["memory_events"] == 36
    assert metrics["query_events"] == 9
    assert metrics["other_events"] == 2
    assert "arms" not in result
    assert ID.load_semantic_bridge_model(model_path)["sha256"] == result["model"]["sha256"]
