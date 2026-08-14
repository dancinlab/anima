import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "state/anima_native_303m_replay_recovery_2026_08_14"
SPEC = importlib.util.spec_from_file_location("native_replay_recovery", HERE / "run_recovery.py")
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_protocol_is_single_mixed_replay_arm_and_blocks_release():
    protocol = module.load_protocol()
    recipe = protocol["fixed_recipe"]
    assert recipe["maximum_training_arms"] == 1
    assert recipe["source_mode"] == "mixed"
    assert recipe["general_fraction"] + recipe["dialogue_fraction"] == 1.0
    assert recipe["endpoint_step"] - recipe["base_step"] == recipe["new_optimizer_steps"]
    assert protocol["bounded_work"]["result_dependent_extension"] is False
    assert protocol["bounded_work"]["participant_mount"].startswith("blocked")
    assert protocol["bounded_work"]["production"] == "blocked"
    assert protocol["gates"]["broad_retention_ce_max"] == 3.4644074976444245
    assert recipe["preprocessing_workers"] == 2


def test_instrument_controls_reject_contradiction_and_korean_substring():
    controls = module.conversation_scorer_controls_result(module.load_protocol())
    assert controls["pass"] is True
    assert len(controls["rows"]) == 8
    assert all(row["pass"] for row in controls["rows"])


def test_training_command_reuses_mixed_response_path(tmp_path: Path):
    protocol = module.load_protocol()
    model = tmp_path / "model"
    data = tmp_path / "data"
    target = data / "data-conversation-target"
    model.mkdir(); target.mkdir(parents=True)
    (data / "manifest.json").write_text(json.dumps({"splits": {
        "train_general": ["general.train"],
        "validation_general": ["general.validation"],
    }}), encoding="utf-8")
    (target / "manifest.json").write_text(json.dumps({"splits": {
        "train_dialogue": ["dialogue.train"],
        "validation_dialogue": ["dialogue.validation"],
    }}), encoding="utf-8")
    command = module.training_command(protocol, model, data, tmp_path / "out", "python")
    assert "--response-only" in command
    assert "--dialogue-only" not in command
    assert command[command.index("--steps") + 1] == "40000"
    assert command.count("--train-general") == 1
    assert command.count("--train-dialogue") == 1


def test_resource_safe_command_preserves_pinned_training_arguments():
    protocol = module.load_protocol()
    command = ["python", "/pinned/train.py", "--steps", "40000"]
    launch = module.resource_safe_training_command(protocol, command)
    assert launch[0] == "python"
    assert launch[1].endswith("/run_pinned_trainer.py")
    assert launch[2:5] == ["--workers", "2", "--"]
    assert launch[5:] == command[1:]


def test_manifest_output_checks_verify_every_consumed_file(tmp_path: Path):
    (tmp_path / "train.txt").write_text("train", encoding="utf-8")
    (tmp_path / "validation.txt").write_text("validation", encoding="utf-8")
    manifest = {
        "splits": {"train_general": ["train.txt"], "validation_general": ["validation.txt"]},
        "outputs": {},
    }
    for name in ("train.txt", "validation.txt"):
        path = tmp_path / name
        manifest["outputs"][name] = {"size": path.stat().st_size, "sha256": module.sha256(path)}
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    checks = module.manifest_output_checks(
        manifest_path, tmp_path, ("train_general", "validation_general"),
    )
    assert len(checks) == 2
    assert all(row["pass"] for row in checks.values())

    (tmp_path / "train.txt").write_text("changed", encoding="utf-8")
    checks = module.manifest_output_checks(
        manifest_path, tmp_path, ("train_general", "validation_general"),
    )
    assert checks["data/train.txt"]["pass"] is False
    assert checks["data/validation.txt"]["pass"] is True


def test_pinned_trainer_resolves_modules_beside_trainer(tmp_path: Path):
    code = tmp_path / "code"
    measurement = code / "measurement"
    measurement.mkdir(parents=True)
    (measurement / "__init__.py").write_text("", encoding="utf-8")
    (measurement / "native_dialogue_registry.py").write_text(
        "NATIVE_DIALOGUE_SPEC={'native_dialogue5': {'preprocessing_workers': 9}}\n",
        encoding="utf-8",
    )
    trainer = code / "train.py"
    observed = tmp_path / "observed.txt"
    trainer.write_text(
        "from measurement.native_dialogue_registry import NATIVE_DIALOGUE_SPEC\n"
        f"open({str(observed)!r}, 'w').write(str(NATIVE_DIALOGUE_SPEC['native_dialogue5']['preprocessing_workers']))\n",
        encoding="utf-8",
    )
    completed = subprocess.run([
        sys.executable, str(HERE / "run_pinned_trainer.py"),
        "--workers", "1", "--", str(trainer),
    ], check=False)
    assert completed.returncode == 0
    assert observed.read_text(encoding="utf-8") == "1"


def test_broad_retention_replays_preregistered_measurement(tmp_path: Path, monkeypatch):
    protocol = module.load_protocol()
    model = tmp_path / "model"
    code = model / "code"
    data = tmp_path / "data"
    checkpoint = tmp_path / "checkpoint"
    code.mkdir(parents=True)
    data.mkdir()
    checkpoint.mkdir()
    for name in ("native_dialogue_lm.py", "train_native_dialogue_lm.py"):
        (code / name).write_text("", encoding="utf-8")
    registry_path = code / "measurement/native_dialogue_registry.py"
    registry_path.parent.mkdir()
    registry_path.write_text("", encoding="utf-8")
    (checkpoint / "final.pt").write_bytes(b"checkpoint")
    (checkpoint / "tokenizer.json").write_bytes(b"tokenizer")
    protocol["parent"]["tokenizer_sha256"] = module.sha256(checkpoint / "tokenizer.json")
    validation_files = [f"validation-{index}.txt" for index in range(12)]
    (data / "manifest.json").write_text(json.dumps({
        "splits": {"validation_general": validation_files},
    }), encoding="utf-8")
    for name in validation_files:
        (data / name).write_text("validation", encoding="utf-8")

    parameter = SimpleNamespace(device="cuda:0")
    fake_model = SimpleNamespace(parameters=lambda: iter((parameter,)))
    observed = {}
    native = SimpleNamespace(
        __file__=str(code / "native_dialogue_lm.py"),
        load_native_model=lambda *_args, **_kwargs: (
            fake_model, object(), {"config": {"block_size": 1024}},
        ),
    )
    class Source:
        def __init__(self, general, dialogue, block_size, seed, fraction):
            observed.update(general=general, dialogue=dialogue, block_size=block_size,
                            seed=seed, fraction=fraction)
    trainer = SimpleNamespace(
        __file__=str(code / "train_native_dialogue_lm.py"),
        load_general_tokens=object(),
        load_corpus_files=lambda paths, tokenizer, loader, workers: (
            observed.update(paths=paths, tokenizer=tokenizer, loader=loader, workers=workers)
            or [1, 2, 3]
        ),
        BatchSource=Source,
        validation_loss=lambda *_args, **kwargs: (
            observed.update(validation_kwargs=kwargs) or 3.25
        ),
    )
    registry = SimpleNamespace(__file__=str(registry_path))
    loaded = {
        "native_dialogue_lm": native,
        "train_native_dialogue_lm": trainer,
        "measurement.native_dialogue_registry": registry,
    }
    monkeypatch.setattr(module.importlib, "import_module", loaded.__getitem__)

    result = module.measure_broad_retention(
        protocol, model, data, checkpoint, "cuda",
    )
    assert result["ce"] == 3.25
    assert result["pass"] is True
    assert result["threshold"] == protocol["gates"]["broad_retention_ce_max"]
    assert observed["workers"] == 2
    assert observed["block_size"] == 1024
    assert observed["seed"] == protocol["audit"]["broad_measurement"]["seed"]
    assert observed["validation_kwargs"] == {
        "source_mode": "mixed", "response_only": False,
    }


def test_execute_uses_requested_model_code_directory(tmp_path: Path, monkeypatch):
    model = tmp_path / "model"
    data = tmp_path / "data"
    target = data / "data-conversation-target"
    (model / "code").mkdir(parents=True)
    (model / "checkpoints/step-035000").mkdir(parents=True)
    target.mkdir(parents=True)
    protocol = module.load_protocol()
    for relative in protocol["source_hashes"]:
        base = data if relative in {"manifest.json", "data-conversation-target/manifest.json"} else model
        path = base / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}", encoding="utf-8")
    for relative in ("checkpoints/step-035000/final.pt", "checkpoints/step-035000/tokenizer.json"):
        (model / relative).write_bytes(b"x")
    monkeypatch.setattr(module, "preflight", lambda *_args: {"pass": True})
    monkeypatch.setattr(module, "training_command", lambda *_args: ["python", "train.py"])
    monkeypatch.setattr(module, "resource_safe_training_command",
                        lambda *_args: ["python", "safe.py", "train.py"])
    observed = {}
    class Completed:
        returncode = 0
    def fake_run(command, cwd, check):
        observed.update(command=command, cwd=cwd, check=check)
        return Completed()
    monkeypatch.setattr(module.subprocess, "run", fake_run)
    monkeypatch.setattr(module.sys, "argv", [
        "run_recovery.py", "--model-root", str(model), "--data-root", str(data),
        "--output", str(tmp_path / "out"), "--execute",
    ])
    assert module.main() == 0
    assert observed == {"command": ["python", "safe.py", "train.py"],
                        "cwd": model / "code", "check": False}
