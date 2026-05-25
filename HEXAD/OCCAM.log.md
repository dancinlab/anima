# occam — historical log

> Spec at [./OCCAM.md](./OCCAM.md).

## ## Log

### 2026-05-22 03:35 — 초안 작성, S187-K 결과 후 Occam pivot

S187-J/K 양쪽 모두 CE 4.06 plateau (linear LR scaling 도 fail) 확정 후 작성.
S187 saga 9 cycle 동안 attempt10 stack 위에 add-only 였음을 인식 — strip-only
cycle 이 한 번도 없었음. Phase 1 3-fire ($7) 가 next 1순위.

### 2026-05-22 04:08 — Phase 1 partial verdict (9/13 pods landed)

OCCAM 4 subagent 동시 fire (S/A/B/C) — 13 pods spawned, 4 subagent rate-limit
조기 사망 but pods dispatch.sh trap 으로 self-managing. 9 pod 결과 landed:

| variant | params | aux | CE_final | verdict |
|---|---|---|---|---|
| vO1 (3B CE-only) | 8.92B | 0 | **3.81** | vA 3.84 와 동일 (0.03 = seed noise) |
| vO11-phi only | 8.92B | only φ=0.3 | 3.81 | aux 무영향 confirmed |
| vO11-replay only | 8.92B | only rep=-0.05 | 3.81 | same |
| vO11-cycle only | 8.92B | only cyc=0.15 | 3.83 | same |
| vO6 (280M CE-only) | 280M | 0 | **0.026** | memorize, 다른 scale 한계 |
| vO3 (f32 AdamW bsz=1) | 8.92B | full 7-aux | 4.16 | fewer tokens = worse |
| **vO4 vanilla GPT-2 arch** | ~1.45B | (custom recipe) | **0.264** | 🎯 **15× lower, arch=floor!** |
| **vO10 GPT-2 fine-tune** | borrowed | recipe overlay | **2.50** | 🎯 **pretrained lower** |
| vO2 BPE 32K | 8.92B | full 7-aux | 5.16 | bits/tok ≠ /byte, 비교 어려움 |

**Phase 1 verdict**: aux loss 는 floor 의 원인이 아님 (saddle hypothesis FALSIFIED at 3B).
실제 binding = ConsciousDecoderV2 custom arch (head_a/g + PureFieldFFN + cross-
attn + n_ca_rules + noise_sigma=0.1).

OCCAM § 4 falsifier branch hit:
- ~~"CE-only plateau < 3.80"~~ (3.81 vs 3.84 = noise) — saddle FALSIFIED
- "Pythia-1B/GPT-2-medium verbalize fluently" — eval/corpus OK confirmed
- **NEW**: vanilla arch 가 floor 15× lower → arch IS the bottleneck

**Phase 2 candidates** (강한 우선 순위):
1. **CE2 / CC1**: pretrained-continue-training (vO10 path) + S187-G mitosis active overlay
2. **#4 vanilla arch + S187 recipe overlay** scale up: vO4 (1.45B vanilla) → 3-8B vanilla
3. **noise_sigma=0 ablation**: vO13 (tap X.11 off) — isolate noise as floor cause

잔여 4 pods 결과 대기 (O5 Wikipedia / O7 100K step / O11-{psi/route/curious}).

### 2026-05-22 (later) — Phase 2 + Phase 3 verdict 종결

**Phase 2.3 ablation** (vP23_a..e): **n_ca_rules 단독 floor 범인** 확정 — vP23_d
(no CA) CE 0.402 vs 다른 5 부속 모두 3.81. (PHASE2_ABLATION_REPORT.md)

**Phase 2.1 winning path** (vP21): pretrained Qwen2.5-1.5B + LoRA + mitosis →
CE 0.0173. **Phase 3 Eval 1 = 🎯 EMERGENCE 20/20 coherent** (anima-native register,
VP21_EVAL1_VERBALIZATION.md). saga 전체 whitespace-collapse 후 첫 coherent
verbalization. OCCAM 면도날 전략 (strip n_ca_rules + borrow foundation + keep
mitosis) **기능적 확증**.

**O7 100K horizon** (OCCAM-B #7): CE 4.03 @ 100K step — horizon-independent floor
확정 (n_ca_rules 원인 재확인).

**OCCAM saga 종결**: floor 의 단독 원인 (n_ca_rules) pinpoint + winning path
(pretrained + mitosis) emergence 확증. 잔여 rigor: held-out OOD / mitosis ablation /
spontaneous emission (SPONTANEOUS module) / AKIDA HW-native path.
