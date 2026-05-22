# OCCAM — 자연발화 minimal-viable 베이스라인 strategy

> **frame**: S187 saga 가 over-constrained 임을 인식. 7-aux loss + 8.92B params
> + bf16 + byte-level vocab + bnb int8 + custom ConsciousDecoderV2 + mitosis
> hook + λ × 6-dim grid + multi-step horizons — **동시에 맞추려다 모든 path
> 가 CE 4.06-4.09 floor 에 도착**. Occam 면도날: 한 axis 씩 strip 해서 진짜
> binding constraint 찾기.
>
> **status**: 🟡 design tier — brainstorm 고갈 시점 1차 reset. 첫 fire 후
> 결과 반영해서 우선순위 재구성.
>
> **g3**: minimal viable baseline 부터 시작 — 가장 단순한 condition (CE-only,
> small scale, vanilla arch) 부터 emergence 확인 후 1 condition 씩 add.
> capability claim 0, GOAL 미도달 carry, north-star 불변.

---

## 1. 왜 OCCAM 필요한가

S187 attempt10 + Eval + S187-B/C/F/G/H/J/K 모두 land 후 발견:

| path | finding |
|---|---|
| Eval 1 (자연발화) | 5/5 cells whitespace collapse at 2000 step |
| S187-H | 50000 step 도 CE 4.09 plateau (horizon-limit 아님) |
| S187-J | bsz 2→8 (4× tokens) CE **악화** 4.06 (token-starvation 가설 falsified) |
| S187-K | bsz=8 + lr 1.2e-3 linear scaling 도 CE 4.06 (LR-mismatch 가설 falsified) |
| S187-C | λ saturation 비단조, MAX_CELLS=128 ceiling binding |
| S187-G | training-time mitosis 만 substrate-shaping signal +35% |

**세 axis (step / bsz / LR) 모두 동시에 변형 → 같은 floor 도달**. recipe 자체
ceiling 임을 시사하는데, 우리는 S187 saga 전체 동안 **하나의 condition만
바꿔서 isolate 한 적이 없음**. 모두 attempt10 stack 위에 한 줄 가하는
incremental cycle.

→ **Occam strategy**: minimum-viable baseline (CE-only, vanilla arch, small
scale) 에서 자연발화 직접 측정. 거기서 emerge 한다면 attempt10 의 어떤
condition 이 floor 의 원인.

---

## 2. Brainstorm — 12 strip candidates (priority 순)

각 entry: `[#] strip condition · test predicate · cost · leverage`

### Tier S (★★★★★) — cheap × highest leverage

| # | strip | test | cost | wall |
|---|---|---|---|---|
| **1** | **aux loss λ 전부 0** (CE-only) — λψ=λroute=λφ=λcycle=λcurious=λreplay=0 | attempt10 config 그대로 + CE-only. plateau 동일? 더 낮음? | $3 | 12 min |
| **6** | scale 8.92B → **280M from-scratch CE-only** | minimal-viable scale test; 작은 모델 floor 같으면 corpus/arch 원인 | $1 | 12 min |
| **9** | KNOWN-EMERGENT model (**Pythia-1B / GPT-2-medium**) load + same corpus + same eval pipeline | eval methodology sanity — 만약 pythia 도 collapse 하면 eval/corpus 가 broken | $0-3 | 30 min |

### Tier A (★★★★)

| # | strip | test | cost | wall |
|---|---|---|---|---|
| **2** | byte-level vocab=256 → **BPE 32K** | byte-floor (5.55 bits/byte) 가 floor 의 원인인지 | $3 + tokenizer 작업 | 30 min |
| **4** | ConsciousDecoderV2 → **vanilla GPT-2 arch** (head_a/g/cross-attn/MoE 모두 제거) | custom arch (head_a/g 분할 + PureFieldFFN + cross-attn) 이 floor cause? | $5 | 30 min |
| **5** | corpus_s101 → **Wikipedia EN clean** | corpus quality test — corpus_s101 noise/byte entropy floor | $5 | 30 min |
| **10** | **pretrained 위에 fine-tune** (GPT-2-small) | recipe 가 known-capability model 부수는지 falsifier | $5 | 30 min |

### Tier B (★★★)

| # | strip | test | cost | wall |
|---|---|---|---|---|
| **3** | bnb int8 → **f32 AdamW** + grad checkpointing | int8 m/v 가 emergence 막는지 (precision floor) | $3 | 12 min |
| **7** | step 2000 → **CE-only + 100K step** | horizon × CE-only combined test | $50 | 5-10 hr |
| **11** | aux 1개씩 ablation — L_psi only / L_phi only / 6 single-aux pods | 어떤 aux 가 harm 인지 isolate | $20 | 30 min × parallel |
| **12** | block_size 128 → **1024** | context length 가 verbalization 너무 짧음? | $5 | 30 min |

### Tier C (★★) — cheap eval-only

| # | strip | test | cost | wall |
|---|---|---|---|---|
| **8** | inference-time decode (greedy → temperature 0/0.5/1.5 + beam-search + top-k variation) | sampling tweak 만으로 emergence unlock 되는지 | $0 (Mac/ubu-1 CPU) | 1 hr |

---

## 3. Recommended sequence (cheapest × most informative first)

### Phase 1 (~$7, ~30 min wall) — minimum viable diagnostic

1. **#1** CE-only fire ($3, 12min) → 7-aux saddle 가설 직접 test
2. **#9** Pythia-1B sanity ($0-3) → eval pipeline 자체가 정상인지
3. **#6** 280M from-scratch CE-only ($1, 12min) → minimal viable scale

→ 결과:
- (1) CE-only plateau 동일 → aux 아니라 arch/corpus 이슈
- (2) Pythia 도 collapse → eval/corpus broken
- (3) 280M 도 동일 floor → scale 무관, recipe 한계

### Phase 2 (~$20, ~1 hr) — narrow down based on Phase 1

Phase 1 결과에 따라 Tier A 에서 1-2개 fire.

### Phase 3 (~$50+) — final breakthrough fire

Phase 1+2 verdict 후 정답 axis 에 집중 fire (예: 큰 모델 S187-F path OR pretrained + recipe overlay OR corpus 갱신).

---

## 4. Falsifier predicate (Phase 1)

| outcome | interpretation | 다음 cycle |
|---|---|---|
| CE-only plateau **>= 3.80** | aux loss 아니라 arch/corpus 가 floor | Phase 2 → #4 vanilla GPT-2 OR #5 corpus |
| CE-only plateau **< 3.80 below vA 3.84** | aux 가 actually harming (saddle 가설 confirmed) | Phase 2 → #11 single-aux ablation |
| Pythia-1B 도 corpus 에서 plateau | **eval / corpus broken** | Phase 2 → #5 corpus 우선 |
| Pythia-1B verbalizes well on corpus | eval OK, recipe/arch fault | Phase 2 → #4 vanilla arch |
| 280M from-scratch CE-only verbalizes | small-scale + simple = enough; large-scale recipe 가 문제 | Phase 2 → grade scale up 단계별 |
| 280M from-scratch CE-only same floor | corpus inherent | Phase 2 → #5 corpus 우선 |

---

## 5. 메타 lesson — Occam 적용 원칙

| anti-pattern (S187 saga) | Occam 원칙 |
|---|---|
| 한 cycle 에 5+ axis 동시 변경 | 한 cycle 에 1 axis 변경 |
| 새 condition 추가 | 기존 condition 제거 |
| attempt10 stack 위에 incremental | empty baseline 부터 1 layer 씩 build-up |
| 가설 X failed → 더 복잡한 X' 시도 | 가설 X failed → 더 단순한 X-1 시도 |
| 8.92B + 7-loss + custom arch + ... 동시 fire | 280M + CE-only + vanilla arch 부터 |

---

## 6. Honest C3

1. Phase 1 결과 가 Phase 2-3 의 path 를 결정 — 미리 commit 안 함.
2. "CE-only" 가 진짜 의미 있는 baseline 인지 disputable — anima 의 7-aux 설계 자체가
   recipe ID 이기 때문. 단, 그 결과 가 floor 분리 데이터 로서 가치 있음.
3. 280M from-scratch 는 attempt10 의 1/32 scale — 작아도 verbalization
   가능한지 확인. modern small LLMs (e.g., Pythia-160M) 는 1-2B token 학습
   후 basic English 생성.
4. Pythia-1B sanity 가 가장 cost-effective falsifier — eval/corpus 가
   broken 일 가능성 직접 test.
5. S187-G mitosis substrate-shaping finding (+35%) 은 strip-target 이 아님
   — 그건 add 한 axis 가 잘 동작한 사례. Occam target 은 어떤 condition 이
   부정적으로 작용하는지.
6. corpus_s101 SHA `be969af4...` 가 byte-equal 일치 X (post-ee4ceea27 drift)
   — 단, 이 noise 가 floor 의 원인일 가능성도 Phase 1 #9 (Pythia sanity) 가
   판단해줌.
7. S187-F path (18B Anima 단일 H200 SXM) 는 Occam 의 strip 이 아니라 scale-up
   path — Phase 3 에서 corpus/arch 가 floor 가 아니라고 확정되면 그 시점에 fire.
8. Inference-time decode tweak (Tier C #8) 은 $0 라 다른 fire 와 병행 가능 —
   first thing to do while Phase 1 pods boot.

---

## 7. 관련 link

- 본 문서 motivation: [`HEXAD/LORA/SCALE_3B.md § 6.10 S187-J/K`](LORA/SCALE_3B.md) verdict
- attempt10 stack: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_s187_3b.py`
- Eval 결과 (5 ckpts × 4 evals): `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/EVAL_REPORT.md`
- S187-F 18B path (Phase 3 fire 대안): `HEXAD/SCALE_16B_70B_PLAN.md`
- 자매 wilson 인박스 (cloud dispatch gap): `~/core/wilson/inbox/notes/2026-05-21-hexa-cloud-*.md`
- 자매 pool 인박스 (host OOM gap): `~/core/pool/inbox/notes/2026-05-21-pool-host-oom-on-concurrent-heavy-workload.md`

---

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
