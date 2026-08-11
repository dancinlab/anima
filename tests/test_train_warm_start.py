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
    def test_bytegpt_random_start_uses_canonical_scale_and_tied_head(self):
        _canonical_train_imports()

        import torch
        from model import ByteGPT, ByteGPTConfig

        torch.manual_seed(20260812)
        model = ByteGPT(ByteGPTConfig(d=64, n_layer=2, n_head=4, block=32))
        self.assertIs(model.head.weight, model.tok.weight)
        self.assertAlmostEqual(float(model.tok.weight.std().detach()), 0.02, delta=0.001)
        self.assertAlmostEqual(
            float(model.blocks[0].attn.in_proj_weight.std().detach()), 0.02, delta=0.001)
        self.assertAlmostEqual(
            float(model.blocks[0].attn.out_proj.weight.std().detach()), 0.01, delta=0.001)
        self.assertAlmostEqual(
            float(model.blocks[0].mlp[2].weight.std().detach()), 0.01, delta=0.001)
        self.assertTrue(torch.count_nonzero(model.blocks[0].attn.in_proj_bias) == 0)

        inputs = torch.randint(0, 256, (2, 32))
        targets = torch.randint(0, 256, (2, 32))
        ce = float(model(inputs, targets)["loss"].detach())
        self.assertLess(ce, 6.0)

    def test_bytegpt_is_causal_and_engine_serialization_matches_torch(self):
        _canonical_train_imports()

        import numpy as np
        import torch
        import decode
        import serialize as serializer
        from model import ByteGPT, ByteGPTConfig

        torch.manual_seed(20260812)
        cfg = ByteGPTConfig(d=32, n_layer=2, n_head=4, block=64)
        model = ByteGPT(cfg).eval()
        original = torch.randint(0, 256, (1, 48))
        changed = original.clone()
        changed[:, 24:] = torch.randint(0, 256, (1, 24))
        with torch.no_grad():
            logits_original = model(original)["logits"]
            logits_changed = model(changed)["logits"]
        self.assertTrue(torch.equal(logits_original[:, :, :24], logits_changed[:, :, :24]))
        self.assertGreater(float((logits_original[:, :, 24:] -
                                  logits_changed[:, :, 24:]).abs().max()), 0.0)

        with tempfile.TemporaryDirectory() as directory:
            pt_path = os.path.join(directory, "tiny.pt")
            bin_path = os.path.join(directory, "tiny.bin")
            torch.save({"model": model.state_dict(), "config": cfg.as_dict(),
                        "step": 0, "val_ce": None, "nparam": model.num_params()}, pt_path)
            serializer.serialize(pt_path, bin_path)
            weights = decode.bg_load(bin_path)
            ids = list(b"causal serializer parity")
            with torch.no_grad():
                torch_logits = model(torch.tensor(ids)[None, :])["logits"][0, :, -1].numpy()
            engine_logits = decode.bg_forward_last_W(weights, ids, len(ids))
        np.testing.assert_allclose(engine_logits, torch_logits, rtol=1e-5, atol=1e-6)

    def test_bytegpt_engine_checkpoint_overwrites_new_initialization_exactly(self):
        _canonical_train_imports()

        import torch
        import serialize as serializer
        from model import ByteGPT, ByteGPTConfig
        from train import _warm_start

        cfg = ByteGPTConfig(d=32, n_layer=2, n_head=4, block=64)
        torch.manual_seed(7)
        source = ByteGPT(cfg)
        torch.manual_seed(11)
        restored = ByteGPT(cfg)
        self.assertFalse(torch.equal(source.tok.weight, restored.tok.weight))

        with tempfile.TemporaryDirectory() as directory:
            pt_path = os.path.join(directory, "source.pt")
            bin_path = os.path.join(directory, "source.bin")
            torch.save({"model": source.state_dict(), "config": cfg.as_dict(),
                        "step": 0, "val_ce": None, "nparam": source.num_params()}, pt_path)
            serializer.serialize(pt_path, bin_path)
            report = _warm_start(restored, bin_path, True, cfg.as_dict())

        self.assertIn("ByteGPT .bin loaded", report)
        for name, tensor in source.state_dict().items():
            self.assertTrue(torch.equal(tensor, restored.state_dict()[name]), name)

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
