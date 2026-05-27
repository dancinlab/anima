"""Re-instantiate the IonQ-seeded HMAC-DRBG (NIST SP 800-90A Rev.1, SHA-256)
and emit 8192 bytes; verify byte-for-byte that the first 1024 bytes match
the recorded ground truth in hmac_drbg_seed.json."""
import hashlib
import hmac
import json
import sys
from pathlib import Path

REPO = Path("/Users/ghost/core/anima")
SRC = REPO / "state" / "nexus_qrng_quantum_seed_2026_05_02"
DST = REPO / "state" / "qmirror_qrng_regression_2026_05_03"

meta = json.loads((SRC / "hmac_drbg_seed.json").read_text())
raw = json.loads((SRC / "quantum_measurement_raw.json").read_text())

entropy = bytes.fromhex(raw["raw_bits_4096_hex"])
nonce = meta["nonce"].encode()
pers = meta["personalization_string"].encode()
expected_first_1024 = bytes.fromhex(meta["first_output_1024_bytes_hex"])


class HmacDrbgSha256:
    OUTLEN = 32

    def __init__(self, entropy: bytes, nonce: bytes, pers: bytes = b""):
        seed_material = entropy + nonce + pers
        self.K = b"\x00" * self.OUTLEN
        self.V = b"\x01" * self.OUTLEN
        self._update(seed_material)
        self.reseed_counter = 1

    def _hmac(self, key, data):
        return hmac.new(key, data, hashlib.sha256).digest()

    def _update(self, provided_data: bytes):
        self.K = self._hmac(self.K, self.V + b"\x00" + provided_data)
        self.V = self._hmac(self.K, self.V)
        if provided_data:
            self.K = self._hmac(self.K, self.V + b"\x01" + provided_data)
            self.V = self._hmac(self.K, self.V)

    def generate(self, n_bytes: int, additional_input: bytes = b"") -> bytes:
        if additional_input:
            self._update(additional_input)
        out = b""
        while len(out) < n_bytes:
            self.V = self._hmac(self.K, self.V)
            out += self.V
        self._update(additional_input)
        self.reseed_counter += 1
        return out[:n_bytes]


drbg = HmacDrbgSha256(entropy, nonce, pers)
out_8192 = drbg.generate(8192)
assert out_8192[:1024] == expected_first_1024, "HMAC-DRBG re-derivation MISMATCH"
sha = hashlib.sha256(out_8192[:1024]).hexdigest()
assert sha == meta["first_output_sha256"], "first_1024 sha256 mismatch"
print(f"HMAC-DRBG re-derivation: OK (first_1024 sha256={sha})")

# Persist 8192-byte stream as one decimal-byte-per-line (matches qmirror dump format)
out_path = DST / "hmac_drbg_legacy_bytes_8192.txt"
with out_path.open("w") as f:
    for b in out_8192:
        f.write(f"{b}\n")
print(f"wrote: {out_path} (n={len(out_8192)})")
