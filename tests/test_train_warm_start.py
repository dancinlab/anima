import importlib.util
import os
import sys
import tempfile
import unittest


TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None


def _canonical_train_imports():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    core_dir = os.path.join(root, "core")
    cli_dir = os.path.join(root, "cli")
    # `cli/evaluate.py` may already have cached the command wrapper under the bare module name
    # `serialize`. These regressions exercise the codec SSOT, so make the same core-first path
    # ordering as cli/train.py explicit and clear only that ambiguous cached import.
    for part in (core_dir, cli_dir):
        if part in sys.path:
            sys.path.remove(part)
    sys.path[:0] = [core_dir, cli_dir]
    sys.modules.pop("serialize", None)


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch training extra is not installed")
class TrainWarmStartTest(unittest.TestCase):
    def test_slw_trailer_is_restored_and_cannot_be_silently_dropped(self):
        _canonical_train_imports()

        import torch
        import serialize as serializer
        from model import CLMConfig, CLMConvMoE
        from train import _warm_start

        cfg = CLMConfig(n_experts=1, n_trunk_layers=1, d_model=8,
                        slw=True, slw_n_slot=2, slw_k=4)
        source = CLMConvMoE(cfg)
        with torch.no_grad():
            source.slw.gamma.fill_(0.375)
            source.slw.K_slots.copy_(torch.arange(8).reshape(2, 4) / 10)

        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "source.clm")
            serializer.serialize_v3(source.state_dict(), 1, 1, path)
            serializer.append_slw_trailer(path, source.slw)

            restored = CLMConvMoE(cfg)
            report = _warm_start(restored, path, False, {"d": 8, "L": 1, "E": 1})
            self.assertIn("SLW=restored", report)
            self.assertTrue(torch.equal(restored.slw.K_slots, source.slw.K_slots))
            self.assertTrue(torch.equal(restored.slw.gamma, source.slw.gamma))

            plain = CLMConvMoE(CLMConfig(n_experts=1, n_trunk_layers=1, d_model=8))
            with self.assertRaisesRegex(ValueError, "carries an SLW trailer"):
                _warm_start(plain, path, False, {"d": 8, "L": 1, "E": 1})

    def test_one_read_clms_can_upgrade_to_canonical_dual_on_same_value_manifold(self):
        _canonical_train_imports()
        import torch
        import serialize as serializer
        from model import CLMConfig, CLMConvMoE
        from train import _warm_start

        common = dict(n_experts=1, n_trunk_layers=1, d_model=8, clms=True,
                      clms_n_slot=2, clms_d_k=4, clms_d_s=4, clms_r=6,
                      clms_d_g=4, clms_val_center=True)
        source = CLMConvMoE(CLMConfig(**common))
        with torch.no_grad():
            source.clms.W_q.weight.fill_(0.125)
            source.clms.val.fill_(0.25)
            source.clms.W_h.weight.fill_(0.375)

        target = CLMConvMoE(CLMConfig(**common, clms_dual=True))

        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "one-read.clm")
            serializer.serialize_v3(source.state_dict(), 1, 1, path)
            serializer.append_clms_trailer(path, source.clms)

            report = _warm_start(target, path, False, {"d": 8, "L": 1, "E": 1})

        self.assertIn("upgraded-3-to-10", report)
        self.assertTrue(torch.equal(target.clms.W_q.weight, source.clms.W_q.weight))
        self.assertTrue(torch.equal(target.clms.val, source.clms.val))
        self.assertTrue(torch.equal(target.clms.W_h.weight, source.clms.W_h.weight))


if __name__ == "__main__":
    unittest.main()
