# .discoveries — 연속 발견 로그

> `*_discovery` / `*_discovery_log` — `/kick` · `/gap` 발견을 매 배치 연속 수행하고
> 결과를 `.discoveries/<slug>.tape` 에 적재 (id · seed · verdict-tier-target).

흐름: 발견 → `CLAIMS.tape` claim → `hexa verify` → `.verdicts/` → `paper_on_discovery` (자유 slug 논문).
발견은 cycle 끝에 몰지 않고 verify 와 병행. 모든 발견은 폐기/의역 없이 기록.
