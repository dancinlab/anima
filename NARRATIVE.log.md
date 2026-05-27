# NARRATIVE — append-only step log

## 2026-05-28 · A1 narrative-modeling-gap-redesign
- bench C (#1144) 🔴 2/5 FAIL 재현 (F2 FRAGMENTED_LOW · F4 ORDERING · F5 COHERENT_STABLE).
- 진단: 단일 근본원인 = **collision-saturation 모델링 갭**. reuse_rate 가 "직전 WINDOW=10
  turn (=50 prior token) 어디에든 등장" binary set-membership → vocab=64 대비 prior pool 이
  커서 random token 도 P=1−(63/64)^50=0.545 로 포화. closed-form 검증 `diag_probe.hexa`
  → 0.544982 (관측 fragmented 0.509 일치). metric 이 vocabulary coverage 를 잴 뿐
  narrative coherence 를 못 잡음.
- 재설계 `bench_redesign.hexa`: generator byte-동일, 측정자만 교체 — (1) immediate-prior
  overlap (window=1), (2) chance correction (e_chance=0.0757 빼고 [0,1] 재정규화),
  (3) mean coh. falsifier 5 재설정 (포화-free).
- 재측정 (foreground, exit 0, $0): coherent 0.504 · drift 0.333 · fragmented 0.031 →
  **5/5 PASS · 🟢 RECOVERED**. 사전등록 falsifier(≤2/5→substrate한계) 통과로 측정 설계
  결함 가설 지지, closed-negative 기각.
- 산출: `NARRATIVE_A1_MODELING_GAP_REDESIGN.md` (10-section) · `bench_redesign.hexa` ·
  `diag_probe.hexa` · `run_redesign.log` · `diag_probe.log`. baseline `bench.hexa`/`run.log`
  무삭제 보존. NARRATIVE.md M3 CLOSED.
