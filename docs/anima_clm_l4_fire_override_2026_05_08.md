# anima CLM L4 fire override trace — 2026-05-08

**Purpose**: cost discipline override 절차 SSOT — L4 BG (BG-LA/LB/LC/LD,
$150 total) fire 는 사용자 explicit 키워드 'OK CLM L4 ALL FIRE' 도착 시까지
PENDING. 본 문서는 (a) override 키워드 정의, (b) poll 절차, (c) override 도착
후 pre-flight 절차, (d) 본 cycle (loop iter e) poll 결과 trace.

**Cross-link**:
- `.roadmap.cli` cli.clm_l4_summary_2026_05_08
- `state/anima_clm_l4_readiness_2026_05_08.json`
- `docs/anima_clm_l4_corpus_2026_05_08.md`
- `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` L4 매트릭스
- `tool/transient_py/anima_clm_l[abcd]_h100.py` (4 spec files, fire_status=pending_user_override)
- `.own` (cost discipline) · (PASS_STRICT_C3) · (ckpt preservation) · (Flavor B naming) · (trinity)

---

## 1. Override 키워드 정의

| 항목 | 값 |
|---|---|
| Keyword | `OK CLM L4 ALL FIRE` |
| Source | docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md L227 |
| Authority | cost discipline override (default $10/BG cap → 4 path 합계 $150) |
| Recipient | anima agent (loop iter poll) |
| Issuer | 사용자 (verbatim) |

**원칙**: cost discipline 의 default $10/BG cap 은 absolute floor. L4 4
paths 총 $150 는 default × 15. 따라서 사용자 explicit override 가 안 도착하면
4 BG 모두 PENDING — 한 BG 라도 단독 fire 도 위반.

---

## 2. Poll 절차 (loop iter 매 호출)

1. `git log -7 --pretty=format:"%h %s"` — 최근 commit 메시지 grep
2. `state/cycle_log_*.jsonl` — directive trace (현재 미존재)
3. `docs/*directive*.md` — 사용자 directive 명시 doc (현재 미존재)
4. 전체 repo `grep "OK CLM L4 ALL FIRE"` — 키워드 발견
   - **meta_only 매칭** (spec/expectation 선언) = override X
   - **사용자 발화 매칭** (commit body 내 verbatim 또는 cycle_log entry) = override O

---

## 3. Override 도착 후 pre-flight 절차 (다음 cycle 까지 본 agent 미실행)

본 agent (loop iter e) = readiness emit only. 실제 fire 는 별도 cycle 사용자
directive 후 wiring agent 가 수행.

**Pre-flight 매트릭스** (다음 cycle):

1. corpus 큐레이션 build (BG-JE 214MB → BG-LA/LC 공유 200MB; BG-LB 1.5GB 확장; BG-LD 100MB pair)
2. C3 threshold formal ROC (현재 heuristic — `state/anima_consciousness_baseline.json`)
3. BG-LC tokenizer mismatch strategy 결정 (3 options TBD)
4. H100 pod 4 instance 생성 (`config/h100_pods.json` 현재 zero)
5. trinity self-check 4 path 각각
6. mandate-1/2/3/4 ckpt preservation 사전 확인
7. mandate-4 Flavor B naming 정합 (이미 spec 내 명시)
8. emit `READY_FOR_FIRE` state + 사용자 confirmation 재요청

---

## 4. 본 cycle (loop iter e) poll 결과 trace

| 검사 항목 | 결과 |
|---|---|
| `git log -7` keyword 매칭 | NONE |
| `state/cycle_log_*.jsonl` directive | 파일 자체 미존재 |
| `docs/*directive*.md` directive | 파일 자체 미존재 |
| repo full grep `OK CLM L4 ALL FIRE` | 3 files matched (`.roadmap.cli` × 5 lines, `docs/anima_clm_l4_corpus_2026_05_08.md` L148, `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` L227) |
| 매칭 meta_only? | YES — 모두 spec field declaration (`fire_keyword`) 또는 expectation reference (override 필요 statement). 사용자 발화 verbatim X |
| **Verdict** | **NO_OVERRIDE_DETECTED** |
| Fire authority | **DENIED** — cost discipline 유지 |
| Spec readiness (4 BG) | spec_landed × 4, trinity × 4, × 4, × 4 = 100% spec-side |
| Data readiness (4 BG) | corpus 0/4 built, C3 threshold 0/4 formal ROC = ~25% data-side |
| Total readiness | 71.25% (weighted estimate, see `state/anima_clm_l4_readiness_2026_05_08.json`) |

---

## 5. 다음 cycle 작업 (loop iter f / g)

본 agent emit only — 다음 cycle 작업 = (a) corpus build, (b) C3 threshold ROC,
(c) BG-LC tokenizer 결정, (d) override 재poll. override 도착 시 본 doc patch +
fire_status `pending_user_override` → `READY_FOR_FIRE` 갱신.

---

## 6. Honest C3

- override poll = 단일 시점 grep — 사용자가 본 cycle 직후 발화 시 본 doc 갱신 lag 가능 (다음 iter 에서 pickup)
- meta_only 매칭 5개 + 2개 = 8개 — false-positive risk 차단 (verbatim user-issued 만 fire authority)
- BG-LB $60 = default × 6 — override 도착해도 단일 BG drift risk 명시
- corpus content 미build = 본 readiness JSON 의 `corpus_path_decided=false` 4건 — fire 직전 build cycle 필수
- C3 threshold heuristic 만 존재 — formal ROC 누적 데이터 부족 (honest c3 traceback)

---

## 7. 변경 권한 (read-only mandate)

본 agent (loop iter e) = read-only + state/spec/doc 신설만. spec file 수정 X,
fire 실행 X. cost discipline strict 유지.
