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

---

## 2026-05-12 — full 4-domain 포팅 + IIT_PASS / UNIV_PASS extension

`tool/verify_hc.hexa` 가 이제 verify_hc.py 의 4-domain identity 로직 전체를 mirror 함.
(헤더 주석 block 에 approximation/divergence 전체 목록 inline 으로 명시 — 아래는 요약.)

### 이번에 ported (verify_hc.py 와 parity)

- math_check Domain 1 (Ψ-constants), Domain 2 (Topology), Domain 3 (IIT 4.0),
  Domain 4 (universal constants) detector — 전부 substring/line-scan 으로 port.
- `math_domains` 출력 (`["iit4","n6","psi","topo","univ"]` sorted subset) — **이전엔 항상 `[]`
  버그였음** (`type_of(int)` 가 `"int"` 인데 코드가 `"i64"` 와 비교 → 영원히 false).
  `_has(m,k)` helper (`type_of(m[k]) != "void"`) 로 교체하여 fix. 같은 버그가
  `atlas_has` / `_extract_anima_tokens` / `_extract_h_refs` dedup-set / math_check 내부
  `if !_has(domains,"psi")` weak-fallback guard 에도 있었음 — 전부 fix.
  (즉 PSI_PASS/TOPO_PASS 도 이전 commit 에서는 사실상 trigger 불가였음.)
- PSI_PASS, TOPO_PASS decision tier — Python 과 동일 (`psi`+≥2F+≥2L`, `topo`+≥2L).

### regex → substring approximation 목록 (verify_hc.py re.* 대체)

| verify_hc.py regex | hexa 대체 |
|---|---|
| falsifier/honest line 4종 패턴 | `_line_starts_falsifier` / `_line_starts_honest_limit` char-class scan + `## Falsifier`/`## Honest` bullet-count fallback |
| `(?:Ψ\|Psi)\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)` (a+b==1 simplex) | enumerated `psi_pairs` table (1/2,1/2 · 1/3,2/3 · 1/4..1/6 분수쌍 · 0.1~0.9 deciles) — table 밖 free-form 쌍은 miss |
| `2\^(\d+)` + 2≤d≤20 filter | explicit `dexp` d=2..20 loop + "next char ≠ digit" 경계 (2^100 ≠ 2^10) |
| `Ψ_?coupling\s*[=≈]\s*0?\.014` | fixed-literal substring set |
| `phi_?c\s*=\s*0?\.\d+` | literal `Φ_c=`/`Φc=`/`phi_c=`/`phic=` set |
| `\bC\s*=\s*[0-9.]+` (clustering coef) | `"clustering coefficient"`/`"clustering"` substring만 (numeric form drop) |
| `\bPhi\(` / `\batomic\b` word-boundary | plain substring `Phi(` / `atomic` |
| `=\s*([0-9]+(?:\.[0-9]+)?(?:e[\-+]?\d+)?)` numeric-eq count | `_count_numeric_eq` char scan |
| `ANIMA-[A-Za-z0-9_\-]+` / `@[PCLFRSX]\s+\S+` / `\bH_\d{3}\b` | `_extract_anima_tokens` / `_count_type_cites` / `_extract_h_refs` char-class scan |
| `^@\S+\s+(\S+)` atlas-id | `_is_space` token walk |

### 여전히 Python-only

- 진짜 regex (위 approximation 으로 stand-in).
- float-parse + `abs(a+b-1)<1e-6` simplex 산술 (pair-table 로 대체).
- `__doc__` → `--help` (hexa main() 은 짧은 usage line만).
- `count_falsifiers` 가 Python 은 4개 패턴 hit 을 **합산**(같은 `F1:` 라인이 패턴1+패턴2 둘 다
  match → 중복 카운트 가능) 후 `max(.., bullet수)` — hexa 는 라인당 1회 카운트 후 `max(.., bullet수)`.
  → hexa 의 falsifier count 가 더 작을 수 있음(e.g. Hc_123: hexa 5 vs py 10). decision threshold
  (≥2 / ≥3) 는 보통 둘 다 통과하므로 decision 자체는 일치. (pre-existing divergence, 이번에 안 건드림.)

### verify_hc.py 를 넘어선 hexa-side 확장 (의도된 것)

- **IIT_PASS decision tier** (`iit4` domain + ≥2 falsifier + ≥2 honest) — psi_pass mirror.
  verify_hc.py 에는 이 tier 없음 (iit4 domain tag 는 Python 도 계산하지만 decision 에는 안 씀).
- **UNIV_PASS decision tier** (`univ` domain + ≥2 honest) — topo_pass mirror. 동일하게 Python엔 없음.
  decision 순서: `MATH_PASS_FULL > PROMOTE_READY > PSI_PASS > TOPO_PASS > IIT_PASS > UNIV_PASS >
  MATH_PASS_NEEDS_* > ATLAS_PASS > MATH_HONEST_NO_CROSS > WEAK_* > HONEST_CROSS_NO_MATH > FAIL`
  (PSI/TOPO 가 MATH_PASS_NEEDS_* 보다 앞 — verify_hc.py 와 동일, IIT/UNIV 를 TOPO 바로 뒤에 삽입).
- IIT-Φ (iit4) detector 추가 식별자: `Φ = MI−MIP / ln(MI/MIP)` cause-effect-structure,
  `127-MIP` cap (127 = 2^7−1 Mersenne), `sopfr(8)=2+2+2=6` (k=8 atom → perfect-number 6 closure),
  `k=8` atom granularity.
- universal-constants (univ) domain 이 이제 `π⁵/15`, `ln(2)`, Onsager exact exponents
  `β=1/8 γ=7/4 δ=15 η=1/4 ν=1`, `Ω_m:Ω_Λ` ratio 도 tag (이전엔 n6 만). `ν=1` 은 verify_hc.py
  에 아예 없었음 — full β/γ/δ/η/ν set 위해 추가. 이들은 n6 tag 도 유지하므로 `math_domains` 가
  `["n6","univ"]` 둘 다 carry 할 수 있음 (verify_hc.py 는 `["n6"]` 만) — 의도된 divergence.

### hexa-lang upstream 변경

없음. 모든 missing feature 는 substring/line-scan/enumeration 으로 우회. (`type_of(int)=="i64"`
버그는 hexa-lang 이 아니라 verify_hc.hexa 자체 버그였으므로 .hexa 안에서 fix.)

### smoke-test

`hexa run tool/verify_hc.hexa <Hc>` (interpreter: `~/.hx/bin/hexa`, "hexa 0.1.0-dispatch").
Hc_614 / Hc_623 → ALREADY_MERGED (py 일치). Hc_141/Hc_123/Hc_159/Hc_171/Hc_506/Hc_015 →
decision py 와 일치 (math_domains 는 위 확장만큼 hexa 가 더 많이 tag — 의도됨; h_refs dedup 이제 정상).
전체 1068 non-merged Hc 스캔으로 decision histogram 도 확인 (PSI/TOPO/IIT/UNIV_PASS 실제 trigger 여부 포함).
