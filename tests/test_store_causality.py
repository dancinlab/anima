import copy
import json

import numpy as np

from cli import evaluate
from core import clms


def _manifests():
    normal = {
        "schema": "anima-storebind/v1",
        "compose": 2,
        "entries": [],
    }
    for gold, a, b in (("good", 0, 1), ("bad", 1, 2)):
        normal["entries"].append({
            "prompt": f"is e{a} and e{b} => ",
            "gold": gold,
            "target_slot": a,
            "target_slot_b": b,
            "store": {"entities": ["e0", "e1", "e2", "e3"], "pols": [0, 1, 0, 1]},
        })
    drop_a = copy.deepcopy(normal)
    drop_b = copy.deepcopy(normal)
    for base, arm_a, arm_b in zip(normal["entries"], drop_a["entries"], drop_b["entries"]):
        arm_a["store"]["entities"][base["target_slot"]] = "zzqqx"
        arm_b["store"]["entities"][base["target_slot_b"]] = "zzqqx"
    drop_a["control"] = "one-slot-only-A-deleted"
    drop_b["control"] = "one-slot-only"
    return normal, drop_a, drop_b


def _write(tmp_path, name, payload):
    path = tmp_path / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def test_store_causality_panel_validates_and_derives_chance(tmp_path):
    normal, drop_a, drop_b = _manifests()
    audit = evaluate._store_causality_load(
        _write(tmp_path, "normal.json", normal),
        _write(tmp_path, "drop_a.json", drop_a),
        _write(tmp_path, "drop_b.json", drop_b),
    )
    assert audit == {"n": 2, "chance": 0.5, "gold_counts": {"good": 1, "bad": 1}}


def test_store_causality_rejects_control_that_changes_more_than_target(tmp_path):
    normal, drop_a, drop_b = _manifests()
    drop_a["entries"][0]["store"]["entities"][3] = "also-changed"
    try:
        evaluate._store_causality_load(
            _write(tmp_path, "normal.json", normal),
            _write(tmp_path, "drop_a.json", drop_a),
            _write(tmp_path, "drop_b.json", drop_b),
        )
    except ValueError as exc:
        assert "replace exactly" in str(exc)
    else:
        raise AssertionError("malformed control was accepted")


def test_store_causality_verdict_requires_all_controls_and_recovery():
    checks, verdict = evaluate._store_causality_decide(0.95, 0.80, 0.50, 0.55, 0.52, 0.80, 0.50)
    assert verdict == "SUPPORTED-CAUSAL"
    assert all(checks.values())

    checks, verdict = evaluate._store_causality_decide(0.95, 0.80, 0.50, 0.70, 0.52, 0.80, 0.50)
    assert verdict == "FALSIFIED"
    assert not checks["drop_b_collapses"]


def test_store_causality_stops_after_failed_pair_oracle(tmp_path, monkeypatch):
    normal, drop_a, drop_b = _manifests()
    paths = [
        _write(tmp_path, "normal.json", normal),
        _write(tmp_path, "drop_a.json", drop_a),
        _write(tmp_path, "drop_b.json", drop_b),
    ]
    calls = []

    def fake_store_run(argv, _return_result=False):
        calls.append(list(argv))
        return {"accuracy": 0.89, "shuffle_integrity": True}

    monkeypatch.setattr(evaluate, "store_run", fake_store_run)
    out = tmp_path / "result.json"
    rc = evaluate.store_causality_run([
        "model.clm", "--store-causality", paths[0],
        "--store-drop-a", paths[1], "--store-drop-b", paths[2],
        "--out", str(out),
    ])

    assert rc == 0
    assert len(calls) == 1
    assert "--store-oracle-pair" in calls[0]
    assert json.loads(out.read_text())["verdict"] == "INVALID-INSTRUMENT"


def test_store_causality_runs_frozen_arm_order_after_oracle_pass(tmp_path, monkeypatch):
    normal, drop_a, drop_b = _manifests()
    paths = [
        _write(tmp_path, "normal.json", normal),
        _write(tmp_path, "drop_a.json", drop_a),
        _write(tmp_path, "drop_b.json", drop_b),
    ]
    calls = []
    scores = iter((0.95, 0.80, 0.50, 0.50, 0.50, 0.80))

    def fake_store_run(argv, _return_result=False):
        calls.append(list(argv))
        return {"accuracy": next(scores), "shuffle_integrity": True}

    monkeypatch.setattr(evaluate, "store_run", fake_store_run)
    rc = evaluate.store_causality_run([
        "model.clm", "--store-causality", paths[0],
        "--store-drop-a", paths[1], "--store-drop-b", paths[2],
    ])

    assert rc == 0
    assert [(call[call.index("--store") + 1], "--store-shuffle" in call,
             "--store-oracle-pair" in call) for call in calls] == [
        (paths[0], False, True),
        (paths[0], False, False),
        (paths[1], False, False),
        (paths[2], False, False),
        (paths[0], True, False),
        (paths[0], False, False),
    ]


def test_dual_address_audit_reports_the_two_consumed_reads():
    d, vocab, n_slot, d_k, d_s, d_g, rank = 4, 256, 4, 3, 2, 2, 3
    rng = np.random.default_rng(10)
    weights = {
        "lane_type": 10,
        "n_slot": n_slot,
        "d_k": d_k,
        "key_emb": rng.standard_normal((256, d_k)),
        "W_q": rng.standard_normal((d, d_k)),
        "W_g": rng.standard_normal((d, d_g)),
        "val": rng.standard_normal((2, d_s)),
        "W_h": rng.standard_normal((d_s + d_g, rank)),
        "b_h": rng.standard_normal(rank),
        "W_out": rng.standard_normal((rank, vocab)),
        "lam": np.asarray([1.0]),
    }
    yn = rng.standard_normal((4, d))
    store = {
        "entities": ["e0", "e1", "e2", "e3"],
        "pols": [0, 1, 0, 1],
        "target_slot": 0,
        "target_slot_b": 2,
        "mention_rows": (0, 1),
        "mention_spans": ((0, 0), (1, 1)),
        "operator_row": 2,
    }
    audit = []

    clms.store_apply(np.zeros((4, vocab)), yn, weights, store, [3], audit=audit)

    assert len(audit) == 1
    assert [read["read"] for read in audit[0]["dual_reads"]] == ["a", "b"]
    assert [read["row"] for read in audit[0]["dual_reads"]] == [0, 1]
    assert [read["span"] for read in audit[0]["dual_reads"]] == [[0, 0], [1, 1]]
    assert [read["target"] for read in audit[0]["dual_reads"]] == [0, 2]
    assert all(0.0 <= read["a_target"] <= 1.0 for read in audit[0]["dual_reads"])
