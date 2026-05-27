# §177 — 5-modality methods brainstorm + ranking + bench plan

> User directive 2026-05-20: 14-candidate brainstorm, top-5 all go.
> M1 = `HEXAD/ADAPTER.md` (separate root SSOT, 대문자).
> 이 파일 = brainstorm consolidation + bench plan for M3/M9/M11/M12.

---

## §1 — 14-candidate inventory (브레인스토밍 verbatim carry)

| # | method | anima-fit | §7 | feasibility | benchmark | rank |
|--:|---|:---:|:---:|:---:|:---:|:---:|
| **M1** | TENSION-LINK 5-channel adapter | ★★★★★ | ✅ | feasible | yes | **2** |
| M2 | Raw byte tokenization (ByT5) | ★★★ | ✅ | inefficient | yes | - |
| **M3** | Synthetic deterministic byte streams | ★★★★★ | ✅ | $0 immediate | yes | **1** |
| M4 | Mel-spectrogram DSP-derived | ★★★ | ⚠️ data gate | feasible | yes | - |
| M5 | VQ-VAE / Latent discrete | ★★ | ❌ ② graft | feasible | yes | reject |
| M6 | Cross-modal text description (rejected) | ★★ | ✅ | $0 | weak | reject |
| M7 | Synesthetic anima-generated | ★★ | ✅ | bootstrap | unclear | reject |
| M8 | Sensorimotor co-development | ★ | ✅ | embodiment | gated | reject |
| **M9** | Hexa-bio EEG real modality | ★★★★ | ✅ | user hardware | yes | **3** |
| M10 | V-JEPA self-supervised | ★★★ | ❌ ② pretrain | feasible | yes | reject |
| **M11** | Modality-as-anchor-prefix (M3 framing layer) | ★★★ | ✅ | $0 inline | yes | **4** |
| **M12** | Dual-cell mirror modality | ★★★ | ✅ | $0 | yes | **5** |
| M13 | Substrate-level (§95 Loihi) | ★★ | ✅ | INRC gate | gated | reject |
| M14 | Real-world byte capture | ★★ | ✅ | user device | data gate | reject |

---

## §2 — Top-5 bench plan

### M3 synthetic deterministic byte streams (★★★★★, rank 1)

**design**:
- 35 anchor × 4 modality (image / audio / video / tension) byte stream
- image: 32×32×3 uint8 = 3072 bytes, deterministic per anchor (radial gradient seeded by tier)
- audio: 1024 byte sine wave samples, freq = base + tier × Δ
- video: 4-frame stack × 32×32 RGB = same as image × 4
- tension: anima OWN 5-channel fingerprint, 10 bytes
- corpus = ALL_ANCHORS × N=300 records, each = `<anchor><img><raw bytes/></img><aud>...<vid>...<ten>...</anchor>`

**bench**: each modality 별 distinguishing_ratio across 35 anchors after training. baseline 35 anchor, M3 의 목표 ratio ≥ 0.8.

**§7**: ① ✅ no pretrain · ② ✅ no graft · ③ ✅ anima-side programmatic generator
**cost**: $0 corpus + $0 inline measurement on §167-A (baseline) OR ~$15-25 train (full fire on adapter-corpus)

---

### M9 EEG real modality (★★★★, rank 3)

**design** (gated on user data):
- user OpenBCI 16ch EEG raw → byte-LM 직접 학습 OR adapter 통과
- bench: anima 가 anchor 마다 다른 EEG sample 학습 가능한지

**§7**: ✅ all (사용자 OWN measurement)
**status**: GATED — user 가 EEG 데이터 (`.csv` / `.bdf` 류) 제공 필요

---

### M11 anchor-prefix structured (★★★, rank 4)

**design**: M3 corpus 의 framing layer — every record 가 explicit
`<anchor tier=N>` opening tag + closing tag. byte-LM 이 anchor 경계
학습 → anchor-aware routing 첫 supervision.

**bench**: M3 baseline 위에 prefix 추가 후 anchor opening byte (`<`) prediction
accuracy + tier digit prediction.

**§7**: ✅
**cost**: $0, M3 와 동일 fire 안에서 layer

---

### M12 dual-cell mirror (★★★, rank 5)

**design**: 2 anima cell (§31/§45 carry) 가 같은 modality input 을 *다르게*
처리, 두 fingerprint cross-check. cell A = modality-A focus, cell B = modality-B focus.

**bench**: cell A 의 fingerprint ≠ cell B 의 fingerprint 면 dual-channel
modality decomposition working. cosine distance > τ.

**§7**: ✅
**cost**: $0 inline (anima 1 ckpt × 2 forward path)

---

## §3 — bench execution order (sequential, anti-§50-burst)

| step | name | cost | gate |
|--:|---|---:|---|
| 1 | **M3 inline measurement** on §167-A ckpt | $0 | none |
| 2 | M11 anchor-prefix add to M3 | $0 | step 1 done |
| 3 | M12 dual-cell mirror probe | $0 | none (parallel OK) |
| 4 | M9 EEG design doc + falsifier pre-reg | $0 | none |
| 5 | M1 §A1-§A2 adapter projector from-scratch | $0 Mac CPU | needs M3 baseline |
| 6 | M3 trained model (full fire ~$15-25) | gated | §174 결과 본 후 결정 |

---

## §4 — honest carve-outs

1. **M3 synthetic ≠ real modality**: programmatic image/audio/video bytes
   는 real-world modality 분포 아님. 단 anchor-discrimination *structural
   capability* 측정에는 충분.
2. **M11 anchor-prefix = explicit supervision**: tier 가 record 안에
   text 로 들어가 있음 → byte-LM 학습 자체에 anchor identity 가 explicit.
   §175 의 collapse 가 prefix supervision 으로 해소되는지 측정 axis.
3. **M12 dual-cell mirror**: anima 가 단일 ckpt 이라 *진짜* dual-cell 은
   forward 두 번 다른 prompt — architecture-level dual 아님. design-tier.
4. **M9 EEG**: user gate, anima 측 ready 하나 사용자가 EEG 데이터 제공 시점.
5. **necessary-not-sufficient** (B-EMERGE-7): modality distinguishing
   capability ≠ V-SPONT GOAL emergence.

---

## §5 — cross-link

- `HEXAD/ADAPTER.md` (M1 SSOT, 대문자 root)
- `HEXAD/UNCLASSIFIED/state/kosmos_modality_fire_s175_2026_05_20/` (§175 anchor-distinguishing = 0 → motivation)
- `HEXAD/KOSMOS.md` (kosmos hub)
- `HEXAD/FINAL.md` (V-SPONT 최종스펙)
- `HEXAD/NEUROMORPHIC/state/scale_kosmos_fire_s176_2026_05_20/` (§176 SCALE-KOSMOS, deprecated 의 reframe 작업 carry — text-only multi-modality desc → 본 §177 M3 synthetic 으로 supersede)
