# hexa port notes (2026-05-12)

## 사용자 directive

> "필요시 hexa-lang upstream 개선가능"

hexa-lang upstream 위치: `/home/summer/core/hexa-lang`

포팅 중 missing feature 발견 시:
1. 포팅 가능한 경우 (substring + line scan 으로 우회) — 우선 해당 방식으로 처리, 한계는 `tool/verify_hc.hexa` 헤더 주석에 명시
2. 우회 불가능한 경우 (e.g. proper regex, JSON encode/decode, hash map iter) — `scripts/hc_verify/HEXA_PORT_BLOCKERS.md` 에 blocker 리스트 작성 → follow-up agent 가 hexa-lang upstream PR 형식으로 처리

## 우선순위 features (verify_hc.py 포팅에 필요)

1. **substring matching** — 있을 가능성 (`.contains()`, `.index_of()`) ✓
2. **regex** — 없을 가능성. fallback: line-by-line + multi-substring check
3. **JSON encode** — atlas_check.hexa 가 사용하므로 있음 ✓
4. **map (dict) iteration** — `for k, v in map { ... }` 패턴 지원 여부 확인 필요
5. **file glob** — `glob("path/*.md")` 필요 (없으면 `read_dir + filter`)
6. **frontmatter YAML parse** — 자체 구현 (single-line key:value 파싱이면 충분)

## 권장 포팅 전략

- v1 (현재): n=6 narrow checker only (no Ψ / Topology / IIT extensions)
- v2 (next cycle): 확장 detectors
- v3 (future): full regex-equivalent (hexa-lang upstream PR 후)
