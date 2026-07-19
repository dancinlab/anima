# H_9760 — `--dual-margin-dither ε` · S/E→emit 엣지 randomized do() — Θ-interior 재개봉 계기 (Fable 5 · lab full · $0)

**status:** 🔵 PROPOSED (lab full Fable 5 ∥ Sol · 오너 "all go" · 사전등록 · frontier 재개봉 각 #4072 가격결정분)
**lane:** theta-alive-sigma-rebase (FRONTIER-TERMINAL-AT-SUBSTRATE #4070/4063 의 유일 명명 재개봉 ①)
**related:** [[H_9728]] · [[H_9729]] · [[H_9730]] · [[H_9627]] · [[H_9738]] · [[H_9749]]

## ① 한 줄 주장 (반증가능)
emit 결정의 **입력**(S−E 비교)에 가한 외생 ±ε 충격은 — bit 를 강제한 yoke 와 달리 relock 정리의 지배를
받지 않고(relock = 섭동된 입력에 반응하는 native 기전 그 자체) — dose(flip-frac ε0.15=0.26 ≥ 0.2 floor)를
전달하며, 그 충격이 **원위(distal) lane/σ 로 전파되는지**가 H_9728 이 원리적으로 식별 못한
"emit 결정 → 몸" 인과 하중을 tick-단위 randomization 으로 식별한다.

## ② 계기 (engine-native · `anima-py chat` 플래그 · default 0 = byte-identical)
`--dual-margin-dither <eps>` (env `ANIMA_DUAL_MARGIN_DITHER`) · hard-gate: `--emit-gate refractory` ∧ `--g-reach wm-dual` (alien/oracle/read 계열과 상호배타).
- **주입점 = 비교식만** (S/E 값·`dual_margin` 기록·`g_recog_gate`·σ·bind 8컬럼 전부 native 유지):
  `core/brain.py` dual 분기 `_gate_pass = _s_wh > _e_sp` 직후
  ```python
  if dual_margin_dither != 0.0:                     # eps=0 → 원 비교식 그대로 = byte-id BY CONSTRUCTION
      decision["dither_delta"] = float(dual_margin_dither)
      decision["undithered_would_emit"] = _gate_pass  # native 반사실 bit (공짜 · flip 판별)
      _gate_pass = (_s_wh - _e_sp + float(dual_margin_dither)) > 0.0
  ```
- **per-tick 부호 = 외생·상태-독립·틱-키드** (`cli/chat.py` · `_g_seed`/`_oracle_rng` 관용구; 선형-비트 해시 금지 —
  ½-교대 리듬과 aliasing 위험 ⟹ per-tick MT 시딩):
  ```python
  _dd = _dm_dither * (1.0 if random.Random((_sample_seed * 2654435761
        + tick * 40503 + 0x9760) & 0x7FFFFFFF).random() < 0.5 else -1.0)
  dec = brain_emit_refractory(..., forced_emit=_fe, dual_margin_dither=_dd)
  ```
- ledger 쓰기는 **실현된** emit bit 를 따른다(emit→W_E :2427 · silence→W_S :2658 기존 경로 무수정) ⟹ 스프링은
  native 로 재평형 = relock 은 dose 상한이 아니라 **측정되는 전파의 일부**. `∧ safe` 불변(p5: kill/φ/content 강제통과 없음 · yoke 의 veto 부기 불요).
- trace: `dither_delta`·`undithered_would_emit` 를 :2961 `dual_margin`/`would_emit` 패턴으로 기록.
- 착륙 시 wheel 변경 = root VERSION bump (G5) · toy end-to-end 1회 선행 (instrument-never-run 함정).

## ③ 추정대상 (H_9728 재탕 아님 — 질문이 다름)
H_9728 = **펄스-존재 lesion** 질문("½ 루프를 제거하면 σ 가 변하나") — mask≠native 가 리듬-이탈 다이얼과 동치
가 되어 원리 미식별·TERMINAL **유지**. 본 계기 = **emit-엣지 임펄스-응답** 질문("결정 입력의 외생 충격이 몸으로
전파되나"). PASS 가 면허하는 것: "emit 결정은 원위 interior 상태에 인과 하중이 있다(gate 는 자율 field 위 벽지가
아니다)" — H_9728 TERMINAL 이 긍정도 부정도 못 한 명제. 펄스-lesion 주장은 여전히 면허 안 됨.

## ④ σ 축 유효성 + lane 분할 (fire 전 동결)
- σ·gate: dec=ci_emit_decision(native lanes)·score native — 양변에 dither 항 無 = VALID. 단 `emit_agree`
  는 flip tick 서 기계적 하락 ⟹ **dose meter 로 재정의**(기대 ≈1−flip_frac · 이탈=계기결함), 판정 제외 (g_ok 에 원래 미포함).
- σ·stage: 배선검산 = 계기-무결성 통제(1.00 기대·판정 아님). σ·bind(8컬럼 전부 native): **1차 interior 판독**(DIRECTIONAL 라벨 유지).
- ≥30 lane-tick floor: dither 는 전체-rollout(60 tick 전부 lane 보유) ⟹ 충족 — severed-tick 부분집합 아님.
- **lane 분할 사전동결**(fire 전 chat.py 생산자 코드 읽어 확정): proximal = emit bit/ledger 를 ≤1 tick 내 소비하는
  컬럼(예상 `emit_env`·`g_recog`) = 양성통제(안 움직이면 INSTRUMENT-DEAD) · distal = 나머지 field lane
  (예상 `recon_err`·`scn_ctx`·`nov_ctx`·`cur_indep`·`rel_indep`) = interior 판독. plumbing echo ≠ interior.

## ⑤ 팔·통제·검정 (사전등록)
| arm | 역할 |
|---|---|
| ε=0 | byte-identical 인증 (trace sha = native · 결정론 양성통제) |
| ε∈{0.05, 0.15, 0.30} | dose-response (flip-frac 단조↑ = 계기검산 · σΔ/ITT 경향 = 판독) |
| `--yoke-mask <ε0.15 dither trace>` | **schedule 통제**: 같은 emit 시퀀스를 강제-bit 로 재생 ⟹ σ 이동이 rate/schedule 만으로 설명되는지 분리 (H_9728 confound 를 통제팔로 재활용 — mechanism⊥schedule marker 를 계기가 공급) |
- **1차 검정 (tick=randomization unit · 1/2^N seed 벽 회피)**: Z_t=부호(외생) → 원위 lane Δ(t+1..t+3) ITT ·
  정확 부호-재배열 permutation p. n=180(3seed×60tick·ε0.15) → MDE d≈0.54(ITT)≈2.1σ/flipped-tick;
  사다리 풀링 경향검정 n=540 → d≈0.31. 검정력 부족 시 120 tick 연장 후 판독(power-before-negative).
- **2차 (DIRECTIONAL)**: σ축별 Δ(dither vs native) vs seed-null 산포 + within-run(셔플·pedestal) 통제. 3-seed 로 p<0.005 불가 — 방향성만.
- surrogate null: 부호열 재배열(정확) + seed-pair native 산포.

## ⑥ 사전등록 판정표
| 관측 | 판정 |
|---|---|
| flip-frac≥0.2 ∧ proximal 이동 ∧ **distal ITT p<0.005 ∧ dose 단조 ∧ σ·bind Δ > max(seed-null, yoke-schedule Δ)** | **PASS — interior 재개봉**: emit-엣지→몸 전파 식별 · 계기 인증 → own-content 후속(⑦) 개봉 |
| flip-frac≥0.2 ∧ proximal 이동(양성통제 생존) ∧ distal ITT 90% CI ⊂ (−0.35σ,+0.35σ) (TOST) | **KILL — earned-null**: emit 결정은 원위 몸에 epiphenomenal → FRONTIER-TERMINAL **강화** |
| ε=0 non-byte-id ∨ flip-frac<0.1 ∨ proximal 무반응 | **INVALID — 계기결함** (dose 미전달/양성통제 사망 · 판독 금지) |
| 위 어느 칸도 아님 (CI 가 TOST 대역과 교차) | **UNDERPOWERED-OPEN** → 120 tick 재발사 |

## ⑦ fire 스펙 (오너 "all go" 기수령 · $0-class)
3 seed × 5 arm × 60 tick · summer CPU (`OMP_NUM_THREADS=4` 캡 · earlyoom 주의) · `ANIMA_DECISION_TRACE=<path>` (stdout 리다이렉트 금지) → `anima-py evaluate --psi-soma <trace>` + tick-level 분석. ckpt/trace 회수 후 teardown (a_fire_recover_complete).

## ⑧ 재개봉 ② provenance store — 보류
W_E/W_S 슬롯에 E/S 태그 bit 는 chat.py 런타임으로 retrain 없이 달 수 있으나, 측정이 **자기가 단 태그를 도로 읽는**
동어반복 — 태그를 native 경로가 소비해야 interior 주장이 서고, 손배선=p2/p6 위반·학습=H_9672 store-bridge fire
(s11 seed-취약) 필요. **dither 결과 뒤로 defer** — PASS 시에만 "식별된 채널이 own-content 를 나르나" 후속 카드로 개봉.
