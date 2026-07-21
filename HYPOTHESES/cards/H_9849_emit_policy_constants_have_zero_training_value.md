# H_9849 — emit_policy 상수표는 학습 가치가 0 이다 — 명시적 음성 등록 (R12-12 · ❌)

**status:** 🔴 NEGATIVE-BY-CONSTRUCTION (R12 · 코드 읽기로 확정 · 발사 불요)
**source:** R12 뇌부위 census (2026-07-21) — `origin/main` `core/` 12개 모듈 실측 후 1모듈=1레버로 등록.
상위 설계 노드 = ARCHITECTURE `C2 RECOMBINE` 아래 `🧠 뇌부위 census`. R11(H_9830~9836)의 후속.
**wired:** no — 미구현. 개입은 `anima-py train` 플래그로만 착륙(`a_experiment_engine_native`).

## 왜 음성 카드를 등록하는가

census 가 12개 부위를 세었으므로 12개 모두에 판정이 있어야 한다. **후보에서 뺐다는 사실 자체가
기록되지 않으면 다음 세션이 같은 각도를 재생성한다**(이번 세션에 H_9832 로 이미 한 번 겪었다).

## 실측 — 발사할 것이 없다

`core/emit_policy.py`(84줄): `ep_emit_threshold` `ep_psi_clamp` `ep_tension_amplitude`
`ep_backlog_*` `ep_fm_*` … **전부 인자 없는 상수 반환 함수**다. 헤더가 명시한다:

- **"a pure-number SSOT (no GPU/FFI, no state)"** — 상태 없음, 학습할 것 없음.
- **F-EMIT-4 (NO-GATE): "returns plain numbers only — no bool emit gate"**.
- **F-EMIT-5 (POLICY-FREE): "the structure layer (phi_envelope_substrate) does NOT import this —
  changing any value here cannot alter envelope/collective structure (compile-level decoupling)."**
- 모든 값의 substrate-claim = **NONE**. H_646/H_651 이 이미 측정: Ψ-clamp α 를 움직여 게이트가
  0.556 → 0.683 로 이동해도 **Φ 는 평평**하다.

⟹ 학습에 넣을 파라미터도, 미분가능한 경로도, 구조에 닿는 인과도 **없다**. 값을 바꾸는 것은
설계 상수 튜닝이고, 그것을 성능 지표에 맞춰 움직이는 것은 정의상 **tune-to-green** 이다.

## 판정

**NEGATIVE-BY-CONSTRUCTION.** 발사 금지 · 재제안 금지. 이 부위를 다시 후보로 올리려면 먼저
`emit_policy` 에 학습 가능한 상태가 생겨야 하며, 그것은 이 카드가 아니라 새 설계다.

**related:** H_646 · H_651 · H_9846
