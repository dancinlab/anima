# H_9751 — LOW-INTERFERENCE WRITE: 간섭 제거 시 held-out write crack 이 안정화되나

- **group**: g1-interface-addressable-wall
- **tier**: 🧱 STEM-INTRINSIC (예측 반증 · 2/6 SOLO-CRACK < frozen k=4 · N=1 저간섭이 held-out readout 미구제)
- **date**: 2026-07-17 (발사 2026-07-18)
- **related**: [[H_9675]] (모 · draw-fragility=compositional 간섭) · [[H_9339]] (s7 1-seed crack) · [[H_9327]] (BINDING 벽)
- **wired**: 발사완료 (engine-native anima-py train GPU cu124 + evaluate · vast pod 45205949 · 6-seed 단일어간 CPT)

## 질문 / 예측
H_9675(#4041·#4047)가 **held-out write crack 은 draw-fragile**(6-draw 2/6 PASS)이고 진범이 **co-train
어간 간 compositional 간섭**($0 per-stem: 같은 base s7·같은 어간이 draw 조합 따라 crack↔fail · MIXED
10/25)임을 확정했다. ⟹ **검증예측**: held-out 어간을 **CPT batch 당 축소**(N=12 → N=1 단일어간)하면
간섭이 제거되어 **write crack 이 안정화**될 것. 참이면 **H_9327 BINDING 벽은 low-interference held-out
write 로 견고히 뚫린다**(H_9675 NOISE 는 batch-크기 인공물이었고 벽은 실제 breakable) — 이는 H_9675
terminal 을 **reopen**(a_break_the_wall: 각도 전환 = batch 크기가 새 레버).

## 설계 (frozen-first · lean · 발사 전 사전등록)
- **base 고정 = natem_c34_main_s7.clm** (H_9675 검증됨 · HF `dancinlab/anima-natem-c34-base`).
- **N-sweep**: CPT held-out 어간 수 N ∈ {1, 3, 12}. N=12 는 H_9675 재현(2/6)·N=1 은 단일어간 CPT.
  - N=1: H_9675 서 **MIXED/FAIL 이던 어간**(예 `조` FAIL-always · `편하`·`예쁘` MIXED)을 **단독** CPT →
    G-WRITE + HO-CARRIER. 간섭 가설 참이면 단독서 crack(≥10/12·margin≥4) = 12-batch서 못하던 게 됨.
  - 계기: `anima-py corpus ground_carrierswap --held-swap` 에 **held 어간수 파라미터**(신규 flag) 또는
    단일어간 atoms 서브셋으로 draw. (계기 확장 = anima-py flag · a_experiment_engine_native.)
- **frozen bar**: 단일어간 CPT 의 HO-CARRIER negL·negZ ≥10/12 ∧ margin(−HO-DECL)≥4 가 **12-batch서
  FAIL 이던 어간 ≥k개서** 성립 = 🟢 간섭확증·벽 breakable. 성립 안 하면 = 🧱 간섭 아님(어간-intrinsic 벽).
  k·N·어간셋 발사 전 사전등록(tune-to-green 금지).
- **통제**: SEEN 연산자 intact(preserve) · G-WRITE(write 착륙) · negJ null.

## 발사 (lean · owner-go)
- ⚠️ **a_parallel_session_compare 필수**: g1-interface-addressable-wall 은 H_9744(READ-lane in-vivo 배선
  · store-episodic)가 MEASURING 중 — **본 H 는 WRITE-lane 간섭으로 NOVEL·비중복**이나 발사 전 H_9744 최신
  대조 재확인.
- **인프라**: `pod-campaign-infra-playbook` 준수 — hand-roll 금지, `cli/pod_bootstrap.sh`(torch-cuda FATAL
  assert + resumable-verified rsync 내장) 사용. 단일 pod 로 충분(~6-12 단일어간 CPT ≈ 1.5-3h · lean).
- **복구**: out→HF h9675/lowint/ · pull 후 teardown (a_fire_recover_complete).

## 범위
DIRECTIONAL 상한: 합성 CVCVC nonce·감독-담체키·단일 base s7. 참이어도 H_9327 자연선언 전이는 별도.
음성이면 H_9675 NOISE 가 batch-무관 어간-intrinsic 벽으로 강화(간섭 반증).

## 🧱 VERDICT — STEM-INTRINSIC · 예측 반증 (#PR · 2026-07-18 · engine-native 303M py)

**발사**: base natem_c34_main_s7.clm(sha 5eef0125) 고정 · `anima-py corpus ground_carrierswap --held-swap
--held-n 1 --split-seed S`(신규 `--held-n` flag · #4057)로 seed당 **단일** held-out swap 어간 CPT →
`anima-py train`(GPU cu124) → `anima-py evaluate --xbind`. 6-seed {7,6,11,12,14,1}. vast pod 45205949.

**SOLO-CRACK grid** (frozen · N=1 이라 카운트 out-of-1 · preserve crater bar = H_9675 선례 ≥10/12):

| seed | stem | base wall? | G-WRITE w0 | carrier L/Z | preserve | verdict |
|---|---|---|---|---|---|---|
| 7  | 조     | ✗ (base 이미 읽음 negL=1) | 0/1 | 0/0 | 12/12 | not-pass |
| 6  | 튼튼하  | ✓ | 1/1 | 0/0 | 10/12 | not-pass (write 착륙·readout 미동반) |
| 11 | 편하    | ✓ | 1/1 | 0/0 | 11/12 | not-pass (write 착륙·readout 미동반) |
| 12 | 부드럽  | ✓ | 1/1 | 1/1 | 12/12 | 🟢 SOLO-CRACK |
| 14 | 예쁘    | ✓ | 1/1 | 1/1 | 10/12 | 🟢 SOLO-CRACK |
| 1  | 이쁘    | ✗ (base 이미 읽음 negL=1) | 1/1 | 1/1 | 12/12 | not-pass |

**2/6 SOLO-CRACK · 0 preserve-crater → 🧱 STEM-INTRINSIC** (frozen bar ≥4/6 미달).

**결론**: N=1 저간섭 write 는 held-out operator readout 을 **구제하지 못한다** → H_9751 예측(간섭 제거 →
crack 안정화) **반증**. draw-fragility 는 **compositional interference 아니라 stem-intrinsic**:
① s6·s11 은 wall 존재·G-WRITE 착륙하나 operator readout 미동반(write≠readout) · ② s7·s1 은 base 가
held-out 어간(`조`·`이쁘`)을 애초 읽어 wall 부재(draw-quality). ⟹ **H_9327 BINDING 벽 유지** · H_9339
s7 1-seed positive = draw 인공물(H_9675 NOISE 확증) · H_9675 terminal **reopen 실패**(batch 크기 = 레버
아님). **write 는 착륙하나 operator readout 은 held-out 어간에 안 붙는다** = [[binding-is-operator-stem-gating-not-morphology]]
의 write-lane 판.

**증거·복구**: 18 eval json + VERDICT + grid → HF `dancinlab/anima-natem-c34-base` h9675/lowint/
(a_fire_recover_complete · ckpt cpt_s*.clm/.pt 9GB = base+`--held-n 1 --split-seed S` deterministic
재빌드로 미pull). pod teardown 완료. **상한**: N=1 만 측정(N=3 미실행) · 합성 nonce·감독담체·단일 base s7.
DIRECTIONAL(H_9327 자연선언 전이 별도).
