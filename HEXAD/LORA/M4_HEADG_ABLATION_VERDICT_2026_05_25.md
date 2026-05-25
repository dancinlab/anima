# M4 head_g ablation — post-wiring 첫 진짜 Δfinal_CE 측정

> 2026-05-25 KST · LORA 도메인 cycle (M4 milestone). PR #507 (H_257 wiring fix)
> 가 head_g axis 를 진짜 wired (aux LM-CE term + `--head-g-weight`) 한 직후, **head_g
> ON vs OFF 의 Δfinal_CE** 를 측정. milestone M4 "각 axis 별 Δfinal_CE 정량"
> 의 **첫 데이터포인트**.
>
> ⚠ cycle 24 교훈 적용 — **SECURE pod preemption** 으로 R8a/R8a'/R8a'' 5000-step
> 완주 0/3. 본 fire 는 **ON-DEMAND COMMUNITY** (SECURE 미사용) 으로 발사.

## § 0. TL;DR

- **판정**: __VERDICT__
- **Δfinal_CE** (ON − OFF) = __DELTA__ nats
- fire: 1× A100 80GB PCIe **COMMUNITY ON-DEMAND** (SECURE 미사용), 단일 pod 2-cell **순차** (corpus·GPU 동일 보장)
- step 수: __STEPS__ (milestone metric = final_CE@5000)
- 비용 actual: __COST__

## § 1. 배경 — 왜 지금 head_g ablation 인가

LORA.md M4:

> M4 — AXIS_MAP-FAN 7-axis env-var wiring fix + 진짜 ablation 측정 (각 axis 별
> Δfinal_CE 정량) · 🔧 wiring fix DONE (PR #507, H_257 완전해소) 단 7축 中
> 2축(head_g·freeze_embed)만 진짜 wired, 4축 TODO[axis-impl]; ablation 재발사 미실행

**핵심 맥락 (LORA.md line 70-72)**: PR #507 이전 head_g 자연실험은 **FALSIFIED
(C2=D byte-equal)** — head_g 토글이 결과를 전혀 안 바꿈 = unwired/inert = trivial
identity = 무효. 즉 "head_g FALSIFIED" 의 옛 결론은 **코드가 inert 했기 때문**이지
head_g 가 실제로 무의미해서가 아니었다.

PR #507 wiring fix:
- `train_p21h_v3.py` line 358-363: `head_g_enable=1` 시 `logits_g` 의 LM CE term
  (`L_ce_g`) 을 `head_g_weight` 가중치로 `L_total` 에 추가. default(enable=0)는 skip
  = 무회귀.
- args → cfg dict (line 738-740) → `run(cfg)` end-to-end thread 확인.
- on-pod 업로드본 검증: `grep -c L_ce_g` = 2, `--head-g-weight` flag present.

본 fire 는 **wiring 후 첫 진짜 toggle 실험** — ON 과 OFF 이 byte-equal 이 아니라
실제 final_CE 차이를 내는지 (= wiring 이 살아있는지 + head_g 가 final_CE 에 영향을
주는지) 측정.

## § 2. Fire 설정 (ON-DEMAND 확인)

| field | value |
|---|---|
| cloud-type | **COMMUNITY ON-DEMAND** (`podFindAndDeployOnDemand`, cloudType=COMMUNITY) — **SECURE 미사용** ✅ |
| pod | 1× NVIDIA A100 80GB PCIe (COMMUNITY on-demand $1.19/hr) |
| 토폴로지 | **단일 pod · 2-cell 순차** (cell-OFF → cell-ON) |
| dispatch | `hexa cloud copy-to/nohup/poll/copy-from` (g8) · pod-create = GraphQL on-demand mutation |
| persistence | training = `hexa cloud nohup` (SSH 끊김 생존) · pod = 수동 retain (teardown 전 pull) |
| corpus | anima corpus_s101 (seed 1337, n=777000) + multi_wiki (en,ko,zh,ru,ja 10MB/lang) — **양 cell 동일 corpus 파일 재사용** |
| base | Qwen/Qwen2.5-1.5B (qwen warm-init) |
| 공통 hyperparams | steps=__STEPS__ · bsz=2 · block=512 · lr=5e-5 · warmup=100 · **seed=1337** · **noise_sigma=0** · **n_kv_head=2** · lambda_mitosis=0.05 · mitosis_max=128 |
| **유일 변수** | **head_g** — cell-ON: `--head-g-enable 1 --head-g-weight 0.1 --head-g-objective lm` · cell-OFF: `--head-g-enable 0` |

**ON-DEMAND 확인**: pod-create mutation = `podFindAndDeployOnDemand` (on-demand, NOT
`podRentInterruptable`/spot). cloudType=**COMMUNITY** only (cascade 에서 SECURE 제거).
cycle 24 의 SECURE preempt 0/3 재발 방지.

**왜 단일 pod 순차 (parallel 대신)**: head_g ablation 은 Δfinal_CE 를 head_g 단독에
귀속시켜야 하는 정밀 측정. 단일 pod 순차 = **corpus 파일 byte-identical + GPU class
identical** 보장 → §7.1/§7.2 (corpus-seed / GPU-drift) caveat 동시 해소. parallel
2-pod 는 wall ~절반이나 corpus·GPU 비동일 risk 가 0.1-nat 정밀 Δ 를 오염. a_wall_first
는 "더 빠른 경로가 정직하게 나을 때" 적용 — 본 ablation 은 정밀도가 wall 보다 우선.

## § 3. Result

| cell | head_g | init_CE | **final_CE@__STEPS__** | wall(s) | verdict | n_strong |
|---|---|---|---|---|---|---|
| **OFF** | enable=0 | __OFF_INIT__ | __OFF_FINAL__ | __OFF_WALL__ | __OFF_V__ | __OFF_NS__ |
| **ON** | enable=1 w=0.1 | __ON_INIT__ | __ON_FINAL__ | __ON_WALL__ | __ON_V__ | __ON_NS__ |

**Δfinal_CE (ON − OFF) = __DELTA__ nats**

## § 4. 판정

__VERDICT_DETAIL__

- **SUPPORTED** 기준: |Δfinal_CE| 가 유의미 (≳ GPU numerical noise floor ~0.01 nats)
  → head_g aux term 이 final_CE 를 실제로 바꿈 = wiring live + head_g axis active.
- **FALSIFIED** 기준: Δfinal_CE ≈ 0 (byte-equal 또는 noise-floor 이하) → head_g
  aux term 이 final_CE (head_a 의 LM CE) 를 바꾸지 못함 = head_g inert-on-final_CE.

## § 5. 비용

__COST_DETAIL__

## § 6. Honest caveats (C3)

1. **단일 head_g_weight=0.1 만 측정** — Δ 가 weight 선형/단조인지는 미측정. weight
   sweep (0.05/0.1/0.3) 은 후속 axis-C2 sweep 으로 분리.
2. **final_CE = head_a 의 LM CE** — head_g aux term 은 logits_g (Engine-G head) 에
   걸리고, final_CE metric 은 logits_a (Engine-A head). 즉 측정값은 "head_g 학습이
   head_a 의 final_CE 에 미치는 간접 효과" (shared backbone gradient coupling). head_g
   자체 CE 직접 측정은 별도 metric 필요.
3. **5000-step = milestone metric** — cost/wall 이 prohibitive 가 아니어서 full
   5000-step 측정 (directional run 불필요). __STEPS_NOTE__
4. **2축 only wired** — curriculum/distill/lang-balanced/contrastive 4축은
   TODO[axis-impl] (ML feature 미구현). 본 데이터포인트는 head_g 단독. freeze_embed
   (axis-D) ablation 은 후속 cycle.
5. **corpus HF version drift** — multi_wiki 는 HF streaming first-N (deterministic
   order) 이나 동일 pod 단일 build 재사용으로 양 cell 간 byte-identical 보장.

## § 7. Cross-references

- `LORA.md` — M4 milestone (line 19)
- PR #507 (`eddc86b55`) — H_257 head_g wiring fix
- `HEXAD/LORA/M4_AXIS_WIRING_FIX_2026_05_25.md` — wiring fix 상세 (PR #507)
- `HEXAD/LORA/QWEN_BASELINE_FINAL_CE_PROTOCOL_2026_05_24.md` — M3 baseline protocol (fire 교훈 carry)
- artifacts: `HEXAD/LORA/state/m4_headg_ablation_2026_05_25/v{cell_on,cell_off}/result.json`
