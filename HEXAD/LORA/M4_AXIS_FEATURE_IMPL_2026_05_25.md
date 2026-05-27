# M4 — AXIS-MAP 4축 ML feature 구현 (curriculum · distill · lang-balanced · contrastive)

@goal: cycle 24 M4 wiring fix(PR #507) 가 7-axis env-var 를 env→cfg→log 까지
연결했으나 ML feature behavior 가 없어 inert 였던 4 축(curriculum / distill /
lang-balanced / contrastive)의 **실제 학습 동작**을 `train_p21h_v3.py` 에 구현.
cfg flag 가 실제로 loss·sampling 을 바꾸도록 하되, **gate-off default 는 무회귀
(byte-identical)** 를 핵심 제약으로 유지. (GPU 재발사 없음 — code PR only.)

- 일자: 2026-05-25
- 선행: `HEXAD/LORA/M4_AXIS_WIRING_FIX_2026_05_25.md` (PR #507, MERGED)
- 라이브 surface: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py`
- 미수정(타 owner): `dispatch_p21h_v3_runpod.sh` (4 축 env-var passthrough 는
  PR #385 에서 이미 land — 확인만, 편집 없음), `LORA.md`/`LORA.log.md` (main 소유)

## 1. 출발점 — PR #507 이후 4 축 상태

PR #507 은 head_g(C/C2)·freeze_embed(D) 2 축만 train-loop 경로를 보유해 실제
WIRED 였고, 나머지 4 축(A/B/E/F)은 ML feature 자체가 없어 wiring(parse+env+cfg+log)
만으론 **inert** (`TODO[axis-impl]`). 본 M4 는 이 4 축의 behavior 를 최소·정직하게
구현한다.

| axis | env-var | 의도 | #507 상태 | M4 결과 |
|------|---------|------|-----------|---------|
| A curriculum | `P21H_CURRICULUM_PHASE_STEPS` | corpus 난이도 phase 스케줄 | inert(TODO) | **구현** (seq-len ramp) |
| B distill | `P21H_DISTILL_TEACHER` | teacher KD | inert(TODO) | **TODO 유지** (teacher 부재) |
| E lang-balanced | `P21H_LANG_BALANCED` | 언어-균형 샘플러 | inert(TODO) | **구현** (per-script round-robin) |
| F contrastive | `P21H_CONTRASTIVE_LANG` | 대조 언어 loss | inert(TODO) | **구현** (SupCon) |

## 2. 축별 구현

### axis-A — curriculum (sequence-length schedule) ✅ 구현

- **방식**: 쉬움→어려움 = 짧은 context→긴 context. 학습 첫 `curriculum_phase_steps`
  step 동안 effective sequence length 를 `min_T=64` → `full_T(block_size)` 로
  `n_phases=4` 단계 geometric ramp.
- **hook**: 신규 `curriculum_block_len(step, phase_steps, full_T)` 가 step 별
  `cur_T` 를 산출 → `sampler.sample_batch(..., cur_T=cur_T)` 가 그 길이로 윈도우
  샘플. ramp 종료(step ≥ phase_steps) 또는 disable(phase_steps=0) 시 `None` 반환.
- **무회귀**: `cur_T=None` 이면 `sample_batch` 가 `T=self.T` 로 진행 → randint
  range·slice length 가 기존과 **동일** → byte-identical 샘플링. default
  `curriculum_phase_steps=0` → 항상 `None`.
- **sound 근거**: 짧은 context = LM 난이도 낮음(의존 거리 짧음)은 표준 length
  curriculum. corpus 재배열 없이 sampler 의 윈도우 길이만 스케줄해 자기완결적.

### axis-B — distill (teacher KD) ⛔ TODO 유지 (faking 금지)

- **미구현 이유**: sound 한 KD term 은 **teacher model 이 in-env 에 로드되어
  logits/soft-target 을 실제로 생성**해야 한다. 본 train script 환경에 teacher
  로딩 경로·체크포인트가 **전무**하다.
- teacher 없이 KL term 을 끼워넣으면 (a) 임의 target 에 대한 가짜 KL 이거나
  (b) self-distill 로 의미가 다른 동작이 되어 **"distill" 의도와 불일치 → faking**.
  task 의 "sound 하게 안 되면 fake 하지 말고 TODO 유지" 에 따라 **TODO 유지**.
- env→cfg→log wiring 은 #507 그대로 보존(값은 도달하지만 loss term 없음).
  `--distill-teacher` help + 코드 주석에 "teacher provisioned 전까지 KD term 없음"
  명시. 진짜 구현은 teacher(예: Qwen2.5 base) 로딩 + per-step teacher.forward +
  KL(student‖teacher) 가 선행되어야 하며 별도 PR.

### axis-E — lang-balanced (per-script sampler) ✅ 구현

- **방식**: corpus 는 flatten 된 단일 토큰 스트림이라 sample 시점엔 언어 구획이
  소실되어 있다. sampler 생성 시 토큰 스트림을 block 크기 윈도우로 1-pass 스캔,
  각 윈도우를 dominant script(en/ko/ja/zh/ru — `native_ratio` 휴리스틱)로 태깅해
  **per-script start-index pool** 구축. `sample_batch` 가 가용 script 를 round-robin
  하며 균형 노출.
- **hook**: `TokenizedSampler(lang_balanced=...)` + `_build_script_pools()` +
  `sample_batch` 의 balanced 분기. `run()` 이 `cfg["lang_balanced"]` 로 thread.
- **무회귀**: default 0 → pool 미구축(`script_pools=None`) → `sample_batch` 가
  **legacy uniform-random 분기**(기존 코드 그대로) → byte-identical. (검증: 300
  step 동안 원본 sampler 와 ctx/tgt/aug 완전 일치.)
- **sound 근거**: 균형 노출 자체가 진짜 학습 분포를 바꿈(저빈도 script over-sample).
  태깅은 실제 토큰 디코딩 기반, 휴리스틱이지만 정직(주석에 명시).

### axis-F — contrastive (aux contrastive loss) ✅ 구현

- **방식**: SupCon(supervised contrastive). per-sequence feature = 모델이 반환하는
  per-layer mean tension `(B, L)` (grad 경로 보유). batch 내 sequence 를 dominant
  script 로 그룹핑해 같은 언어=positive / 다른 언어=negative.
- **hook**: 신규 `contrastive_lang_loss(feat, langs)` + `sampler.window_langs(ctx)`
  (디코딩 기반 per-seq script, RNG 미소비=샘플링 결정성 불변) → `L_total` 에
  `contrastive_w * L_con` 가산.
- **무회귀**: default `contrastive_lang=0.0` → `if contrastive_w > 0.0` 가드로 term
  **전체 skip** → loss·optimizer 동일. 또한 batch 에 같은-언어 pair(≥2 member) 가
  없으면 grad-safe 0 텐서 반환 → 가짜 gradient 없음(정직한 degradation).
- **honest 한계**: default `bsz=2` 에선 같은-언어 pair 형성이 드물어 term 이 자주
  0 일 수 있다. 의미 있는 contrastive 신호엔 큰 bsz + lang-balanced 동시 사용
  권장(주석/문서에 명시). 그래도 구조는 sound(구조 부재 시 0, 부재 아닐 시 실제 손실).

## 3. 무회귀(gate-off byte-identical) 보증 — 핵심 제약

모든 4 축 env unset / flag=default → **loss·optimizer 경로 불변**:

| axis | default | gate-off 동작 |
|------|---------|---------------|
| A | `curriculum_phase_steps=0` | `cur_T=None` → `T=self.T` → 동일 randint range/slice (byte-identical) |
| B | `distill_teacher=""` | loss term 자체 없음 (구현 안 함) |
| E | `lang_balanced=0` | `script_pools=None` → legacy uniform-random 분기(기존 코드) |
| F | `contrastive_lang=0.0` | `if contrastive_w > 0.0` 가드 → term skip |

검증(로컬, $0, GPU 없음):
- `python -m py_compile train_p21h_v3.py` → **PASS**
- gate-off sampler 300-step ctx/tgt/aug 원본 대비 **byte-identical PASS**
- curriculum ramp 64→512 단조 + phase 후 `None` **PASS**
- contrastive: positive pair 없음→0.0 grad-safe / 있음→유한 손실+실 gradient,
  B<2→0.0 **PASS**

## 4. 미수정 / scope 밖

- `dispatch_p21h_v3_runpod.sh`: 4 축 env-var passthrough(PR #385) 이미 존재 →
  **편집 없음**(타 agent owner). 따라서 env→dispatch→train→loss 전체 경로가 구현된
  3 축(A/E/F)에 대해 dispatcher 추가 변경 없이 닫힘.
- head_g(C/C2)·freeze_embed(D) 2 축: #507 의 진짜 동작 코드 **무수정**.
- `LORA.md`/`LORA.log.md`: main 소유, 미수정.

## 5. 다음 step (이 PR 범위 밖)

- A/E/F 3 축의 **진짜 ablation 재발사** (init→final CE Δ 변별, ⚠ GPU 비용) — 별도 agent.
- axis-B distill: teacher(Qwen2.5 base 등) in-env 로딩 + KL(student‖teacher) term —
  별도 PR. 그 전까지 TODO[axis-impl] 마커 유지.
- contrastive(F) 의미화: `bsz` 상향 + `lang_balanced=1` 동시 사용 권장 ablation.
