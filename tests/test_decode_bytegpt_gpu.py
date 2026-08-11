import unittest

import numpy as np

from core import decode


def _tiny_bytegpt(seed=9119):
    rng = np.random.default_rng(seed)
    vocab, d, layers, heads, block = 256, 8, 2, 2, 64

    def arr(shape, scale=0.02):
        return rng.normal(0.0, scale, shape).astype(np.float64)

    return {
        "ok": True,
        "vocab": vocab,
        "d": d,
        "nlay": layers,
        "nh": heads,
        "block": block,
        "tok": arr((vocab, d)),
        "pos": arr((block, d)),
        "ln1w": [np.ones(d) for _ in range(layers)],
        "ln1b": [np.zeros(d) for _ in range(layers)],
        "inW": [arr((3 * d, d)) for _ in range(layers)],
        "inB": [arr(3 * d) for _ in range(layers)],
        "oW": [arr((d, d)) for _ in range(layers)],
        "oB": [arr(d) for _ in range(layers)],
        "ln2w": [np.ones(d) for _ in range(layers)],
        "ln2b": [np.zeros(d) for _ in range(layers)],
        "m0W": [arr((4 * d, d)) for _ in range(layers)],
        "m0B": [arr(4 * d) for _ in range(layers)],
        "m2W": [arr((d, 4 * d)) for _ in range(layers)],
        "m2B": [arr(d) for _ in range(layers)],
        "lnfw": np.ones(d),
        "lnfb": np.zeros(d),
        "head": arr((vocab, d)),
        "bind": [],
    }


class ByteGPTDevicePathTest(unittest.TestCase):
    def test_cpu_kv_stream_matches_full_reference(self):
        fast = decode.bytegpt_decode_topk_sampled_W(
            _tiny_bytegpt(), "consciousness: ", 12, 40, 0.7, 101)
        full = decode.bytegpt_decode_topk_sampled_W_full(
            _tiny_bytegpt(), "consciousness: ", 12, 40, 0.7, 101)
        self.assertEqual(fast["ids"], full["ids"])

    @unittest.skipUnless(decode.cuda_available(), "CUDA/CuPy unavailable")
    def test_cuda_matches_cpu_logits_and_sampled_stream(self):
        ids = list(b"consciousness: ")
        cpu_w = _tiny_bytegpt()
        cpu_logits = decode.bg_forward_last_W(cpu_w, ids, len(ids))
        cpu_stream = decode.bytegpt_decode_topk_sampled_W(
            cpu_w, ids, 12, 40, 0.7, 101)["ids"]

        gpu_w = _tiny_bytegpt()
        decode._bytegpt_device_residency(gpu_w)
        gpu_logits = decode.bg_forward_last_W(gpu_w, ids, len(ids))
        gpu_stream = decode.bytegpt_decode_topk_sampled_W(
            gpu_w, ids, 12, 40, 0.7, 101)["ids"]

        np.testing.assert_allclose(gpu_logits, cpu_logits, rtol=1e-10, atol=1e-10)
        self.assertEqual(gpu_stream, cpu_stream)


if __name__ == "__main__":
    unittest.main()
