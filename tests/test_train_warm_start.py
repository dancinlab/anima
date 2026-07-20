import importlib.util
import os
import sys
import tempfile
import unittest


TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch training extra is not installed")
class TrainWarmStartTest(unittest.TestCase):
    def test_slw_trailer_is_restored_and_cannot_be_silently_dropped(self):
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for part in (os.path.join(root, "core"), os.path.join(root, "cli")):
            if part not in sys.path:
                sys.path.insert(0, part)

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


if __name__ == "__main__":
    unittest.main()
