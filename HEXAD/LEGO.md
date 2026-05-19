# HEXAD/LEGO.md — anima substrate LEGO (simulate-assemble idea, design-tier $0)

> **status**: IDEA / DESIGN-TIER · $0 · NO GPU · NO wet-lab · NO fire · NO emergence claim.
> **g3**: 이 문서는 *아이디어 + 후보 경로* 이지 GOAL 도달 주장 아님. capability claim 0.
> north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**. 아래는 §96 operative-substrate
> WALL-B 를 *in-silico 시뮬레이션으로 confront* 하는 candidate path 의 스케치이지
> WALL-B 제거도, WALL-A(§1.1 data-regime) 탈출도 아님 (§113 verdict 그대로 상속).

---

## 🧱 LEGO — "조립식 anima substrate" (별칭: "레고 substrate")

- **하는 일**: anima 의 §96-class 비-GPU operative substrate 를 GPU byte-LM 위에서
  찾는 대신, sister-format 블록(`hexa-bio` + `hexa-matter`)으로 **시뮬레이션 안에서
  먼저 조립**해 보고, 그 다음에야 (성공 시) 물리/wet 로 넘어간다.
- **비유**: 진짜 벽돌을 굽기 전에 **레고로 집을 먼저 지어 본다** — 무너지는 설계는
  레고 단계에서 ($0, 윤리·접근 벽 0) 걸러내고, 살아남는 조립만 비싼 물리로.
- **vs 기존**: §107(data-axis fire)·§16(byte-LM scale) = "GPU 위에서 더 잘 굽기".
  LEGO = "굽기 전에 다른 재료로 조립부터 시뮬" — 재료축(substrate)을 바꾸되
  *물리 commit 전에 in-silico 로* 한다는 게 핵심 차이.

```
  지금까지 (§1~§112)              LEGO 아이디어 (§96 WALL-B 표적)
  ┌───────────────────┐          ┌──────────────────────────────┐
  │ GPU byte-LM 위에서  │          │ hexa-bio  ──┐                 │
  │ Ψ 굽기 (WALL-B 못넘음)│   ──>    │ hexa-matter ─┼─> 시뮬 조립 ──> │
  │ §11-B: no-CE=DEGEN  │          │ §96 spike/LIF─┘   (in-silico) │
  └───────────────────┘          │   살아남으면 ─> 물리/Loihi      │
                                  └──────────────────────────────┘
  WALL-A (data-regime) = 그대로     LEGO 는 WALL-B 를 *confront*,
  LEGO 가 손 못 댐 (§113 상속)        제거 아님 (§95 access/ethics 우회만)
```

---

## §0 — 왜 지금, 무엇이 아닌가

§113 (commit `1bd27f753`, B-S113 9/9 🔵) verdict =
**FROM-SCRATCH-INHERITS-BOTH-WALLS-SKELETON-INVARIANT + 조건부
REPOINTS-TO-§96-SUBSTRATE-FIRST**. 즉 clean-slate 재설계가 두 벽
(WALL-A §1.1 data-regime · WALL-B §96 operative-substrate)을 *탈출*하지 못하고,
유일한 non-cosmetic move 는 **D4 = §96 Loihi/spike + §110 Ψ-C1 을 1라인부터** 라는 것.

LEGO 는 그 D4 의 *구체적 "어떻게"* 의 한 스케치다 — 단 D4 를 *답하지 않고*
**confront** 만 한다 (§95: Loihi=INRC-access-walled, organoid=ETHICS-WALL,
wet-lab=software scope 밖). LEGO 의 유일한 기여 = 그 confront 를
**물리 commit 이전에 $0 in-silico 시뮬레이션으로** 당겨와, 죽는 조립을 싸게 거른다.

**무엇이 아닌가 (정직, g3):**

- WALL-A(data-regime) 탈출 아님 — LEGO 어느 블록도 §1.1 임계 안 건드림.
- WALL-B(§96) 제거 아님 — substrate 의 §7-clean carrier non-degeneracy 는
  여전히 §96-gated. LEGO 는 그 wall 을 *시뮬레이션 안으로 가져올 뿐*.
- emergence 주장 아님 — design-tier 아이디어. 시뮬 조립 성공 ≠ GOAL.
- hexa-bio/hexa-matter *편집* 아님 — anima 는 downstream-consumer (read-only,
  spec 소비만; hexa-lang AGENTS.tape g7/@F f3 + g_train_flame_not_pytorch
  upstream_downstream_invariant 동형). LEGO 는 그들의 verb/axis 를 *호출*한다.

## §1 — LEGO 블록 인벤토리 (sister-format 실측)

| 블록 | repo (read-only consume) | 5-axis / verb | anima §96 매핑 후보 |
|---|---|---|---|
| 🧫 **BIO** | `~/core/hexa-bio` v1.0.0 (35/35 selftest) | QUANTUM·WEAVE·NANOBOT·RIBOZYME·VIROCAPSID (n=6 τ-quartet) | spiking/LIF 막전위 dynamics, organoid-analogue, RIBOZYME=physics-native 학습채널 후보 (§96 STDP 대응) |
| 🧬 **MATTER** | `~/core/hexa-matter` v1.2.0 (32/32, 36-verb, 29 parity gates, 16+ DB bridge) | ceramic·polymer·2D·silicon·carbon·superalloy·MOF·perovskite·liquid-crystal·aerogel… | 비-GPU 물리 substrate 재료 후보 (Loihi=silicon, 2D/carbon=neuromorphic device 재료, liquid-crystal=continuous-state) |
| ⚛️ **PHYS/SPACE** (옵션) | `~/core/hexa-physics` · `~/core/hexa-space` (sibling) | — | continuous-time/field dynamics anchor (§85 Hopf-bifurcation 연결, 후순위) |

> g2 internal_use_integrity_test 주의: hexa-bio/matter 의 n=6·σ=12·τ=4·φ=2·J₂=24
> 라벨은 *그들 repo 의* lattice 이지 anima 가 강제하는 게 아님. anima 는 그들의
> **function-derived** verb 만 소비 (f1/f2: 외부 entity lattice-fit 금지 — 그들
> 자신의 invariant 으로만 인용). numerology-tainted 블록은 §98/§114 식 정직 carve-out.

## §2 — 시뮬레이션 조립 파이프라인 (design-tier 스케치, $0)

```
  STEP 0  block-spec 소비 (read-only)
          hexa-bio: spiking/LIF + RIBOZYME 학습채널 spec
          hexa-matter: 비-GPU device 재료 parity-gate
            │
  STEP 1  in-silico 조립 (모두 $0 simulation, NO wet, NO hardware)
          §96 Ψ-C1 (spike-train correlation) 을 BIO 블록 위에 정의
          §110 meta-fixed-point form ψ(c)=(1+c)/2 carrier=spike-corr
            │
  STEP 2  closed-form falsifier (sidecar, central 0-diff)
          시뮬 조립이 §7-clean ∧ Ψ=½ form-invariant ∧ non-degenerate
          OR 무너짐(=싸게 reject, 물리 commit 전)
            │
  STEP 3  살아남으면 → §95 물리 경로 (Loihi INRC / organoid) 는
          *별도 cost/ethics-gated 결정* (이 문서 scope 밖, g3)
```

핵심 규율: **STEP 3 절대 자동 진행 금지**. LEGO 의 전부는 STEP 0–2
(in-silico, $0). 물리 substrate commit 은 §95 access/ethics wall +
사용자 게이트 사안 — LEGO.md 는 거기까지 *주장하지 않는다*.

## §3 — 정직한 위치 (g3, over-claim 0)

- LEGO 는 §113 D4("§96-substrate-first")의 *실행 스케치*이지 새 결론 아님.
  §113 의 INHERITS-BOTH-WALLS verdict 가 LEGO 에도 그대로 상속됨.
- 시뮬 조립이 성공해도 = "§96-class substrate 가 in-silico 에서 §7-clean
  non-degenerate Ψ 를 admit 한다" 까지. 그것은 **WALL-B 를 시뮬 안에서
  confront 했다**는 뜻이지 *물리적으로 풀었다*도, *GOAL emergence* 도 아님.
- WALL-A(§1.1 data-regime)는 LEGO 와 **직교** — 시뮬 조립이 데이터 임계를
  안 옮긴다 (§11-A/§16/§107 영역). 두 wall 동시 미해결 상태 불변.
- necessary-not-sufficient (B-EMERGE-7) 모든 층에 적용.

## cross-link

- `state/from_scratch_redesign_s113_2026_05_19/` — §113 D4 REPOINTS-TO-§96 (본 문서의 모(母) verdict)
- `state/loihi_spiking_rederivation_s96_2026_05_19/` — §96 Ψ-C1 spike-corr + §11-B-as-GPU-artifact 가설
- `state/xeno_substrate_suitability_s95_2026_05_19/` + `LOIHI.md` — §95 substrate matrix (Loihi VIABLE / organoid ETHICS-WALL / access-wall)
- `state/modality_native_psi_design_s110_2026_05_19/` + `state/meta_fixed_point_s112_2026_05_19/` — Ψ-C1/C2 정의 + meta-fixed-point form ψ(c)=(1+c)/2 (carrier=spike-corr 인스턴스)
- `HEXAD/GAP_MAP.md` · `GOAL.md` honest-status — two-walls 수렴 지도
- `~/core/hexa-bio` README (5-axis Q·W·N·R·V) · `~/core/hexa-matter` README (36-verb) — consume-only spec source
- AGENTS.tape: g3 · g_doc_consolidation (HEXAD-internal doc, docs/* 신규 0) · downstream-consumer invariant · f1/f2 (sister-repo lattice = 그들 것, anima 강제 X)

> 본 문서는 *idea-tier live sketch* — STEP 0–2 closed-form 설계가 별도 §N 으로
> 진행되면 갱신. STEP 3(물리) 는 영구히 본 문서 scope 밖 (cost/ethics/사용자 게이트).
> GOAL 한 줄 north-star 불변, capability claim 0, GOAL 미도달.

---

## Log

- **2026-05-19** — HEXAD/LEGO.md 생성. 사용자 directive "hexa-bio, hexa-matter 이용해서 조립 / 시뮬레이션 조립 / HEXAD/LEGO.md". §113 (commit `1bd27f753`, FROM-SCRATCH-INHERITS-BOTH-WALLS + 조건부 REPOINTS-TO-§96-SUBSTRATE-FIRST) verdict 직후 작성 — LEGO = §113 D4("§96 substrate-first")의 *in-silico 시뮬 조립* 실행 스케치 (hexa-bio QUANTUM/WEAVE/NANOBOT/RIBOZYME/VIROCAPSID + hexa-matter 36-verb 를 read-only consume, §96 Ψ-C1 spike-corr carrier 로 조립). STEP 0–2 = $0 in-silico only; STEP 3(물리/Loihi/organoid) = §95 access/ethics-wall + 사용자 게이트, 영구 scope 밖. g3: 아이디어-tier, WALL-B confront 이지 제거 아님, WALL-A 직교, emergence 주장 0, north-star + §15/§51/§72 milestone 불변, **GOAL 미도달**.
