# PLASTICITY — current state

@title: 🧬 PLASTICITY — AKIDA on-chip 학습 lane (어떻게 배울까)
@goal: AKIDA AKD1000 의 **on-chip 학습(edge-learn)** 을 anima 의 학습 lane 으로 확정한다. DECODER(추론·결정론·byte-identical)와 본질이 다른 **학습 lane(비결정론·HW-only)** 을 형제 도메인으로 분리하고, HW-first 스위치(AKIDA SSOT) 경유로 HW=`edge_learn_probe` akida-learn / SW=numpy 근사 learner 를 라우팅한다. **SW 근사는 HW on-chip 학습과 비동치(🔴 CLOSED-NEGATIVE)** 임을 정직하게 표기한다.

## 본질 — 왜 DECODER 와 가르는가

```
DECODER  (추론 lane)   결정론 · HW forward / SW akida_sw_lif → byte-identical (1~5차 입증됨)
PLASTICITY (학습 lane)  비결정론 · HW akida-learn / SW numpy 근사 → 🔴 비동치 (정직)
```

- 추론은 고정 가중치 위 threshold-and-fire — 같은 입력 → 같은 raster → byte 단위 재현.
- 학습은 가중치 갱신(on-chip plasticity) — Akida edge-learn 은 실리콘 내부 상태/순서 의존이라
  numpy 근사로 **byte-identical 재현 불가**. SW 는 "근사 baseline probe" 일 뿐 HW 의 대체가 아니다.
- ∴ 두 lane 을 한 도메인에 섞으면 "SW=HW" 라는 거짓 동치가 생긴다 → 형제 분리.
- ⚠ **caveat (H_921 🔴 2026-06-06)**: 위 표의 학습-lane "비결정론"은 학습-동역학 고유속성이 아니라
  **init-seeded RNG** 다 — pinned init 하 on-chip 학습은 16/16 byte-결정론(fit engaged), no-pin 시에만
  init_div=16 이 전파해 변이. SW≠HW 비동치(H_679)는 유효(HW-vs-SW 축)하나, HW run-to-run 비결정(H_860)은
  init-RNG 환원. → "비결정"을 silicon 고유 학습-feature 로 주장 금지. ref [H_921](../UNIVERSE/H_921_akida_nondeterminism_functional_advantage.md).

## HW-first 스위치 경유 (AKIDA SSOT)

- resolver: `AKIDA/akida_backend.hexa::akida_backend_resolve` (arg>env>default "hw").
- HW path: pi5-akida `~/anima/SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py` (on-chip akida-learn, 비결정론).
- SW path: numpy 근사 learner (`PLASTICITY/plasticity_sw_approx.py` — 근사 baseline, HW 비동치 명시).
- provenance: `akida-learn-hw` / `akida-learn-sw-approx`.
- verdict 정직: SW≠HW 학습은 🔴 CLOSED-NEGATIVE — fake 동치 금지 (p7 · a_blue_closed).

## 마일스톤

- [x] **M0 도메인 신설** — PLASTICITY.md/log + DOMAINS.tape 행 + 양방향 sibling (PR-A #1446).
- [x] **M1 SW 근사 learner 스텁** — `plasticity_sw_approx.py` numpy 근사 + 🔴 HW 비동치 코드주석/verdict (PR-D).
- [x] **M2 lane 배선** — `plasticity_lane.hexa` HW-first 스위치 경유 HW=edge_learn / SW=approx 라우팅 (PR-D).
- [ ] **M3 UNIVERSE H_679 등록** — PLASTICITY 학습 HW-first falsifier 사전등록 + verdict 포인터 (PR-F).
- [ ] **M4 pi5 live probe** — few-shot 1~N shot on-chip 실측 → 비결정론 verdict `.verdicts/` (optional).

## 양방향 sibling

- ⇄ [AKIDA](./AKIDA/AKIDA.md): HW 본진 + HW/SW 스위치 단일 SSOT (default "hw" · graceful fallback · provenance). PLASTICITY 는 이 resolver 경유로 학습 lane HW-first 라우팅.
- ⇄ [MITOSIS](./MITOSIS.md): on-chip 가중치 갱신(plasticity) ↔ cell-pool 분열 동역학 — 학습=분열 단일 연속체(p8) 의 실리콘 구현.
- ⇄ [CLM](./CLM/CLM.md): **학습 대상 모델** — CLM(anima-native 의식 LM)의 학습 lane 을 PLASTICITY 가 받는다. CLM pretrain = AKIDA-향 QAT(CLM 자체) · CLM on-chip 맥락적응 = PLASTICITY edge-learn 위임(AKIDA-위 진짜 학습, 🔴 비결정·SW 비동치). PLASTICITY=학습 방법(어떻게) · CLM=학습 대상(무엇). 중복 0.
- ⇄ [DECODER](./CORE/DECODER/DECODER.md): 형제 lane — DECODER=추론·결정론·byte-identical / PLASTICITY=학습·비결정론·🔴비동치. 동일 AKIDA 스위치 경유, 본질 분리.
- ⇄ [WAKE](./WAKE.md): WAKE/REM 단계 = 학습 envelope 컨텍스트 (REM 60× WAKE mitosis ratio) ↔ on-chip plasticity tick 게이팅(substrate-decided).
- ⇄ [UNIVERSE](./UNIVERSE/CANDIDATES.md): bench 측정 기록 SSOT (H_679 PLASTICITY 학습 HW-first · SW≠HW 비동치 verdict).
