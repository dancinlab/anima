import importlib
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "cli"))
train = importlib.import_module("train")


def test_deterministic_training_is_explicit_and_native():
    prior = torch.are_deterministic_algorithms_enabled()
    try:
        torch.use_deterministic_algorithms(False)
        train.configure_deterministic_training(False, "cpu")
        assert not torch.are_deterministic_algorithms_enabled()
        train.configure_deterministic_training(True, "cpu")
        assert torch.are_deterministic_algorithms_enabled()
    finally:
        torch.use_deterministic_algorithms(prior)
