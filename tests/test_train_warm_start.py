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
    def test_canonical_lr_schedule_has_exact_warmup_peak_and_cosine_floor(self):
        _canonical_train_imports()
        from train import scheduled_lr

        values = [scheduled_lr(step, 3e-4, "cosine", 4, 12, 0.1)
                  for step in range(1, 13)]
        self.assertAlmostEqual(values[0], 7.5e-5)
        self.assertAlmostEqual(values[3], 3e-4)
        self.assertLess(values[4], values[3])
        self.assertTrue(all(a >= b for a, b in zip(values[3:], values[4:])))
        self.assertAlmostEqual(values[-1], 3e-5)
        self.assertAlmostEqual(scheduled_lr(99, 3e-4, "cosine", 4, 12, 0.1), 3e-5)

    def test_legacy_lr_schedule_remains_constant_without_warmup(self):
        _canonical_train_imports()
        from train import scheduled_lr

        self.assertEqual(scheduled_lr(1, 3e-4, "constant", 0, 20, 0.0), 3e-4)
        self.assertEqual(scheduled_lr(20, 3e-4, "constant", 0, 20, 0.0), 3e-4)

    def test_pinned_hf_corpus_uri_requires_commit_and_preserves_full_filename(self):
        _canonical_train_imports()
        from train import _parse_hf_corpus_spec

        parsed = _parse_hf_corpus_spec(
            "hf://datasets/dancinlab/anima-corpus@abc123/data/train.bytes")
        self.assertEqual(parsed, {
            "repo_id": "dancinlab/anima-corpus",
            "revision": "abc123",
            "filename": "data/train.bytes",
        })
        for invalid in (
            "hf://datasets/dancinlab/anima-corpus/data.bytes",
            "hf://datasets/dancinlab/anima-corpus@main/data.bytes",
            "hf://datasets/dancinlab/anima-corpus@abc123/../data.bytes",
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                _parse_hf_corpus_spec(invalid)

    def test_clm_warm_start_rejects_trunk_norm_forward_mismatch(self):
        _canonical_train_imports()

        import serialize as serializer
        from model import CLMConfig, CLMConvMoE
        from train import _warm_start

        source = CLMConvMoE(CLMConfig(n_experts=1, n_trunk_layers=1, d_model=8,
                                      trunk_norm="global"))
        target = CLMConvMoE(CLMConfig(n_experts=1, n_trunk_layers=1, d_model=8,
                                      trunk_norm="position"))

        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "global.clm")
            serializer.serialize_v3(source.state_dict(), 1, 1, path)

            with self.assertRaisesRegex(ValueError, "changes the forward pass"):
                _warm_start(target, path, False,
                            {"d": 8, "L": 1, "E": 1, "trunk_norm": "position"})

            restored = CLMConvMoE(CLMConfig(n_experts=1, n_trunk_layers=1, d_model=8,
                                            trunk_norm="global"))
            report = _warm_start(restored, path, False,
                                 {"d": 8, "L": 1, "E": 1, "trunk_norm": "global"})
            self.assertIn("trunk_norm=global", report)

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

    def test_exact_resume_matches_uninterrupted_optimizer_and_rng_trajectory(self):
        _canonical_train_imports()

        import random
        import torch
        from train import _restore_resume_state, resume_state_digest

        torch.manual_seed(41)
        base = torch.nn.Sequential(
            torch.nn.Linear(4, 5), torch.nn.Dropout(0.25), torch.nn.Linear(5, 2))
        initial = {k: v.detach().clone() for k, v in base.state_dict().items()}

        def fresh():
            model = torch.nn.Sequential(
                torch.nn.Linear(4, 5), torch.nn.Dropout(0.25), torch.nn.Linear(5, 2))
            model.load_state_dict(initial)
            return model, torch.optim.AdamW(model.parameters(), lr=1e-2, weight_decay=0.0)

        def update(model, optimizer, generator):
            x = torch.randn(3, 4, generator=generator)
            y = torch.randn(3, 2, generator=generator)
            optimizer.zero_grad(set_to_none=True)
            torch.nn.functional.mse_loss(model(x), y).backward()
            optimizer.step()

        full, full_opt = fresh()
        full_gen = torch.Generator().manual_seed(73)
        torch.manual_seed(97)
        random.seed(101)
        for _ in range(4):
            update(full, full_opt, full_gen)

        interrupted, interrupted_opt = fresh()
        interrupted_gen = torch.Generator().manual_seed(73)
        torch.manual_seed(97)
        random.seed(101)
        for _ in range(2):
            update(interrupted, interrupted_opt, interrupted_gen)

        model_state = {k: v.detach().cpu() for k, v in interrupted.state_dict().items()}
        optimizer_state = interrupted_opt.state_dict()
        rng = {
            "torch_cpu": torch.get_rng_state(), "torch_cuda": [],
            "python": random.getstate(),
            "generators": {"data": interrupted_gen.get_state()},
        }
        digest = resume_state_digest(model_state, optimizer_state, 2, rng)
        payload = {
            "optimizer": optimizer_state, "completed_step": 2,
            "rng": rng, "state_digest": digest,
        }

        resumed, resumed_opt = fresh()
        resumed.load_state_dict(model_state)
        resumed_gen = torch.Generator().manual_seed(999)
        step, restored_digest = _restore_resume_state(
            payload, resumed, resumed_opt, {"data": resumed_gen}, "cpu")
        self.assertEqual(step, 2)
        self.assertEqual(restored_digest, digest)
        for _ in range(step, 4):
            update(resumed, resumed_opt, resumed_gen)

        for name, tensor in full.state_dict().items():
            self.assertTrue(torch.equal(tensor, resumed.state_dict()[name]), name)


if __name__ == "__main__":
    unittest.main()
