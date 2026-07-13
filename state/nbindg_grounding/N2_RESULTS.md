# NBIND-G N2 — 측정 결과 (진행중 · 2026-07-13)

동결 스펙 = [`N2_STATUS.md`](N2_STATUS.md). 판정표·게이트는 **데이터 전에 고정**됐고 여기서 바꾸지 않는다.
원본 채점 JSON = [`N2_EVAL/`](N2_EVAL/) (전량 · tail 절단 금지 · `evaluate-py-1`).

## 4-arm 학습 (T=105,169 step · 전부 완주 or 진행)

| arm | seed | 학습 | ckpt 회수 | 호스트 |
|---|---|---|---|---|
| main-s7 | 7 | ✅ 완주 | ✅ | 렌트 pod |
| main-s11 | 11 | ✅ 완주 | ✅ | 렌트 pod |
| base_only | 7 | ✅ 완주 | ✅ | 렌트 pod |
| shuffle_grid | 7 | ⏳ 67% | — | summer |

## held-out D-acc (n=174 · `n2_eval_manifest.json` · gen=8 win=64)

Δ는 동결 스펙대로 **`max(control, 0.50)` 대비** — 우연 바닥 0.50 이 하한이다.

| arm | D-acc | Δ vs 0.50 | margin_med | flip0 (부정없음·극성만) | flip1 (부정있음·XOR) |
|---|---|---|---|---|---|
| main-s7 (seed 7) | 0.477 | **−0.023** | −0.533 | 0.450 † | 0.552 † |
| main-s11 (seed 11) | 0.316 | **−0.184** | −0.534 | **0.391** | 0.241 |
| base_only | 0.000 | 바닥 0.50 적용 | +1.462 | 0.000 | 0.000 |
| shuffle_grid | ⏳ | | | | |

† main-s7 flip 분해는 부분 rows(118/174) 기반 예비치 — 완전판 재채점 진행중.

**`base_only = 0.000` 은 유효성 파탄이 아니다.** filler 만 본 모델은 `긍정.`/`부정.` **형식 자체를
못 낸다**(극성을 틀리는 게 아니라 그 어휘를 출력하지 않음). 동결 스펙이 Δ 기준을 `max(control, 0.50)`
으로 미리 잡아둔 이유가 이것이다 — 바닥은 우연 0.50 이다.

## 읽기 (동결 판정표 · `N2_STATUS.md` §5)

- **NAT-CRACK 🟢 = 미충족**: 양 seed 모두 Δ ≥ +0.20 이 아니라 **우연 미만**(−0.023 · −0.184).
- **MODEL-🧱 가지 진입** → flip0/flip1 분해가 어느 벽인지 지목:
  - `flip0 낮음 = GROUNDING-🧱` / `flip0 높음 + flip1 낮음 = operator-transfer MODEL-🧱`
  - 실측 main-s11 **flip0 = 0.391 < 0.50** ⇒ **GROUNDING-🧱 쪽**.
- 뜻: 격자 XOR 연산자는 설치됐는데(main-s7 seen D-acc **0.950** ≥ 0.85 게이트 PASS),
  held-out 자연 원자의 **극성 자체가 미접지**라 연산자가 적용될 좌항이 없다.
  H_9286 의 "grounding 은 DATA-blocked" 진단과 같은 방향.

## 확정 전 남은 동결 게이트

1. **main-s11 seen ≥ 0.85** (grid 설치 확인 · 미충족이면 under-exposed INVALID) — 채점 진행중.
2. **shuffle_grid**: 학습 67% → coin-seen ≥ 0.85 (control liveness) + held-out.
   이게 없으면 `format-without-operator` 대조가 비어 **FORMAT-🧱 과 구분 불가**.
3. main-s7 완전판 flip 분해 (현재 부분 rows).

이 셋이 채워지기 전에는 verdict 를 박지 않는다 (frozen-first · no tune-to-green).

## 측정 인프라 (판정과 격리 · `infra-wall-noneval`)

- 렌트 pod(192-thread EPYC)는 **다른 임차인이 load average ~106 으로 포화** → 항목당 12분+
  (전용 호스트 4.3s/item 의 **170배**). 174문항 채점이 5시간 동안 진행 줄 0개.
  ⟹ 채점 전량을 summer(12코어 5.4GHz · load ~2)로 이전, arm 당 ~10분에 착지.
- 이 침묵이 진단을 막았던 근본원인 = `--xbind` 가 25문항마다만 진행을 찍은 것 →
  **1번 항목 하트비트 + s/item + eta** 로 수정(0.13.11 · convergence `evaluate-py-9`).
- pod 의 cupy 는 `libnvrtc.so.12` 부재로 커널 컴파일 실패 → GPU 경로가 발화 후 즉사했다.
  capability 게이트를 커널-스모크로 정직화(0.13.10 · convergence `decode-py-1` 확장).
  채점은 canonical numpy 경로(TERMINAL-eligible)라 측정 손실 0.
