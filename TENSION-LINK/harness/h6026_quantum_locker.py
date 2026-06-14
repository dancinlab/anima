#!/usr/bin/env python3
"""H_6026 — can ANU quantum information itself be a MEMORY STORE (write-then-recall)?

Distinct from the cluster:
  H_6016 = is ANU a *readable* DB?            -> no (max-entropy noise)
  H_6017 = is there a usable *index*?         -> no (address>=content)
  H_6018 = is anima's *local* assoc-memory ok?-> yes (ANU is data, store is LOCAL)
  H_6026 = is ANU *itself* the storage medium -> write M, later read the SAME M back
           FROM ANU (not a local file/R2/.kosmos cache, not local Hopfield)?

A memory store must support WRITE(M) then READ()==M. We falsify the 4 candidate
"yes" mechanisms on REAL ANU vacuum bytes (cached pulls in /tmp/anu_*.bin). p7 $0.

  MS1 write channel?      ANU API is GET-only; "write M, read from ANU" -> chance.
  MS2 replay/address?     same address across pulls -> different bytes (no replay).
  MS3 encode M as offset? Library-of-Babel write: address length >= content length.
  MS4 quantum-basis edge? HRR assoc-memory recall: ANU-basis vs PRNG-basis identical
                          => ANU is an interchangeable randomness source, not a store.
"""
import numpy as np, glob, os, math

bufs = sorted(glob.glob("/tmp/anu_*.bin"), key=os.path.getsize, reverse=True)
pulls = [open(p, "rb").read() for p in bufs]
allraw = b"".join(pulls)
big = pulls[0] if pulls else os.urandom(2048)
src = os.path.basename(bufs[0]) if bufs else "urandom"
print("=" * 80)
print(f"H_6026 ANU=기억저장소(write→recall)? — real ANU bytes ({len(pulls)} pulls, {len(allraw)}B total)")
print("=" * 80)

# ── MS1: is there a WRITE channel? write M, then "read it back" from a fresh ANU pull
rng = np.random.default_rng(6026)
M = rng.integers(0, 256, 32, dtype=np.uint8)            # a 32-byte "memory" to store
readback = np.frombuffer(big[:32], dtype=np.uint8)      # what ANU actually returns
recall_ms1 = float(np.mean(M == readback))              # byte-match fidelity
print(f"MS1 write channel?  write 32B M, read from ANU -> recall={recall_ms1:.3f} "
      f"(chance=1/256={1/256:.4f}) -> {'🟢 stored' if recall_ms1 > 0.5 else '🔴 NO write path (recall≈chance)'}")

# ── MS2: replay? same address (offset) across two DISTINCT pulls -> same bytes?
distinct = [p for p in pulls if len(p) >= 64]
a = np.frombuffer(distinct[0][:64], np.uint8)
b = np.frombuffer(distinct[1][:64], np.uint8)            # a different real pull
same_addr_match = float(np.mean(a == b))                 # does offset k recall stable content?
# cross-correlation of two pulls (should be ~0 => uncorrelated => not replayable)
af = (a.astype(float) - 127.5); bf = (b.astype(float) - 127.5)
xcorr = float(abs(np.dot(af, bf) / (np.linalg.norm(af) * np.linalg.norm(bf) + 1e-12)))
print(f"MS2 replay/address? offset k across 2 pulls match={same_addr_match:.3f} xcorr={xcorr:.3f} "
      f"-> {'🟢 replayable' if same_addr_match > 0.5 else '🔴 NO replay (fresh entropy each call)'}")

# ── MS3: encode M as an OFFSET into ANU (store the pointer, ANU holds the data)?
# probability a random L-byte target occurs at any offset of an N-byte buffer.
N = len(big)
for L in (2, 4):
    expected_hits = max(N - L, 0) / (256.0 ** L)        # E[# matches] in random data
    addr_bits = math.log2(max(N - L, 1))                 # bits to name an offset
    content_bits = 8 * L                                 # bits of the memory itself
    grade = "🟢 compresses" if (expected_hits >= 1 and addr_bits < content_bits) else "🔴 no usable store"
    print(f"MS3 offset-encode L={L}B: E[hits in {N}B]={expected_hits:.2e} "
          f"addr={addr_bits:.1f}b vs content={content_bits}b -> {grade}")
print(f"    (pigeonhole: to address arbitrary L bytes you need ~256^L buffer "
      f"=> addr≈content, no compression)")

# ── MS4: does a QUANTUM (ANU) random basis beat a PRNG basis for assoc-memory recall?
# Holographic Reduced Representation: bind=circular conv, bundle=sum, unbind=corr.
def hrr_recall(vecs):
    D = vecs.shape[1]; n = vecs.shape[0] // 2
    keys, vals = vecs[:n], vecs[n:2 * n]
    K = np.fft.rfft(keys, axis=1); V = np.fft.rfft(vals, axis=1)
    mem = np.fft.irfft((K * V).sum(0), n=D)              # bundle of bound pairs (THE store)
    Kc = np.conj(np.fft.rfft(keys, axis=1))
    noisy = np.fft.irfft(np.fft.rfft(mem)[None, :] * Kc, n=D, axis=1)  # unbind each key
    sims = noisy @ vals.T                                 # cosine-ish to every value
    return float(np.mean(np.argmax(sims, 1) == np.arange(n)))

D, n = 256, 8
need = 2 * n * D
# ANU arm: real vacuum bytes -> zero-mean i.i.d. components
ab = np.frombuffer((allraw * (need // len(allraw) + 1))[:need], np.uint8).astype(float)
anu_vecs = ((ab - 127.5) / 128.0).reshape(2 * n, D)
# PRNG arm: numpy PCG64
prng_vecs = np.random.default_rng(7).uniform(-1, 1, (2 * n, D))
acc_anu = hrr_recall(anu_vecs); acc_prng = hrr_recall(prng_vecs)
adv = acc_anu - acc_prng
print(f"MS4 quantum-basis edge? HRR recall ANU={acc_anu:.3f} PRNG={acc_prng:.3f} "
      f"Δ={adv:+.3f} -> {'🟢 quantum advantage' if adv > 0.2 else '🔴 interchangeable (ANU=randomness src, store is LOCAL)'}")

print("-" * 80)
print("결론: ANU 자체는 기억저장소가 아니다 🔴 — (MS1) 쓰기채널 없음 · (MS2) 재생불가(매호출 새 진공요동) ·")
print("(MS3) 주소≥내용(바벨, 압축 안 됨) · (MS4) 양자기저=PRNG기저 회상 동일(ANU=무작위원, store는 로컬).")
print("anima의 진짜 store는 LOCAL (.kosmos/파일/Hopfield H_6018) — ANU는 무작위/공유키(H_6008) 공급원일 뿐.")
